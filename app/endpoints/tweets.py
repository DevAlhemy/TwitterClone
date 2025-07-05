from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy import select, func, desc, insert, delete
from core.security import get_current_user, get_db, User
from sqlalchemy.ext.asyncio import AsyncSession
from db import Tweet, Like, Follow, Media
from sqlalchemy.orm import selectinload
from schemas import TweetCreate


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_tweet(
    tweet_in: TweetCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Создает новый твит для текущего пользователя.

    Args:
        tweet_in: Данные для создания твита (текст и ID медиа)
        db: Асинхронная сессия БД
        current_user: Текущий аутентифицированный пользователь

    Returns:
        {"result": bool, "tweet_id": int} - ID созданного твита

    Raises:
        401: Если пользователь не аутентифицирован
    """
    new_tweet = Tweet(user_id=current_user.id, content=tweet_in.tweet_data)

    if tweet_in.tweet_media_ids:
        result = await db.execute(
            select(Media).where(Media.id.in_(tweet_in.tweet_media_ids))
        )
        media_objects = result.scalars().all()
        new_tweet.attachments.extend(media_objects)

    db.add(new_tweet)
    await db.commit()
    await db.refresh(new_tweet)

    return {"result": True, "tweet_id": new_tweet.id}


@router.delete("/{tweet_id}", status_code=200)
async def delete_tweet(
    tweet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Удаляет твит по ID, если он принадлежит текущему пользователю.

    Args:
        tweet_id: ID твита для удаления
        db: Асинхронная сессия БД
        current_user: Текущий аутентифицированный пользователь

    Returns:
        {"result": bool} - Результат операции

    Raises:
        403: Если твит не принадлежит пользователю
        404: Если твит не найден
        401: Если пользователь не аутентифицирован
    """
    result = await db.execute(
        select(Tweet).where(Tweet.id == tweet_id)
    )
    tweet = result.scalar_one_or_none()

    if tweet is None:
        raise HTTPException(status_code=404, detail="Tweet not found")

    if tweet.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not your tweet")

    await db.delete(tweet)
    await db.commit()

    return {"result": True}


@router.post("/{tweet_id}/likes", status_code=201)
async def like_tweet(
    tweet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Добавляет лайк текущего пользователя к твиту.

    Args:
        tweet_id: ID твита для лайка
        db: Асинхронная сессия БД
        current_user: Текущий аутентифицированный пользователь

    Returns:
        {"result": bool} - Результат операции

    Raises:
        401: Если пользователь не аутентифицирован
    """
    stmt = insert(Like).values(user_id=current_user.id, tweet_id=tweet_id)

    await db.execute(stmt)
    await db.commit()

    return {"result": True}


@router.delete("/{tweet_id}/likes")
async def unlike_tweet(
    tweet_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Удаляет лайк текущего пользователя с твита.

    Args:
        tweet_id: ID твита для удаления лайка
        db: Асинхронная сессия БД
        current_user: Текущий аутентифицированный пользователь

    Returns:
        {"result": bool} - Результат операции

    Raises:
        401: Если пользователь не аутентифицирован
    """
    stmt = delete(Like).where(
        Like.user_id == current_user.id,
        Like.tweet_id == tweet_id
    )

    await db.execute(stmt)
    await db.commit()

    return {"result": True}


@router.get("", response_model=dict)
async def get_feed(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Получает ленту твитов пользователей, на которых подписан текущий пользователь.

    Args:
        db: Асинхронная сессия БД
        current_user: Текущий аутентифицированный пользователь

    Returns:
        {
            "result": bool,
            "tweets": List[{
                "id": int,
                "content": str,
                "author": {"id": int, "name": str},
                "likes": List[{"user_id": int, "name": str}],
                "attachments": List[str]
            }]
        }

    Raises:
        401: Если пользователь не аутентифицирован
    """
    try:
        following_result = await db.execute(
            select(Follow.following_id)
            .where(Follow.follower_id == current_user.id)
        )
        following_ids = following_result.scalars().all()

        if not following_ids:
            return {"result": True, "tweets": []}

        stmt = (
            select(
                Tweet,
                User.name.label("author_name"),
                func.count(Like.user_id).label("likes_count")
            )
            .join(User, Tweet.user_id == User.id)
            .outerjoin(Like, Like.tweet_id == Tweet.id)
            .where(Tweet.user_id.in_(following_ids))
            .group_by(Tweet.id, User.name)
            .order_by(desc("likes_count"))
        )

        stmt = stmt.options(
            selectinload(Tweet.attachments),
            selectinload(Tweet.liked_by).load_only(User.id, User.name)
        )

        result = await db.execute(stmt)
        tweets_data = result.all()

        tweets_out = []
        for tweet, author_name, likes_count in tweets_data:
            likes_info = [
                {"user_id": user.id, "name": user.name}
                for user in tweet.liked_by
            ]

            attachments = [f"/media/{media.file_path}" for media in tweet.attachments]

            tweets_out.append({
                "id": tweet.id,
                "content": tweet.content,
                "author": {
                    "id": tweet.user_id,
                    "name": author_name
                },
                "likes": likes_info,
                "attachments": attachments
            })

        return {"result": True, "tweets": tweets_out}

    except Exception as e:
        return {
            "result": False,
            "error_type": "database_error",
            "error_message": str(e)
        }
