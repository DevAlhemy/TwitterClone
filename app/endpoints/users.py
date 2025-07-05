from core.security import get_current_user, get_db, User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from schemas import UserResponse
from db import Follow


router = APIRouter()


@router.post("/{id}/follow")
async def follow_user(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Подписаться на пользователя.

    Args:
        id: ID пользователя для подписки
        db: Асинхронная сессия БД
        current_user: Текущий аутентифицированный пользователь

    Returns:
        {"result": bool} - Результат операции

    Raises:
        400: Bad Request - если:
            - Попытка подписаться на себя
            - Уже подписаны на пользователя
        401: Unauthorized - если пользователь не аутентифицирован
    """
    if current_user.id == id:
        raise HTTPException(status_code=400, detail="Cannot follow yourself")

    stmt = insert(Follow).values(follower_id=current_user.id, following_id=id)
    try:
        await db.execute(stmt)
        await db.commit()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Already following")

    return {"result": True}


@router.delete("/{id}/follow")
async def unfollow_user(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> dict:
    """
    Отписаться от пользователя.

    Args:
        id: ID пользователя для отписки
        db: Асинхронная сессия БД
        current_user: Текущий аутентифицированный пользователь

    Returns:
        {"result": bool} - Результат операции

    Raises:
        401: Unauthorized - если пользователь не аутентифицирован
    """
    stmt = delete(Follow).where(
        Follow.follower_id == current_user.id,
        Follow.following_id == id
    )
    await db.execute(stmt)
    await db.commit()
    return {"result": True}


@router.get("/me", response_model=UserResponse)
async def get_me(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """
    Получить профиль текущего пользователя.

    Args:
        db: Асинхронная сессия БД
        current_user: Текущий аутентифицированный пользователь

    Returns:
        UserResponse: Полная информация о пользователе включая:
            - Основные данные
            - Список подписчиков
            - Список подписок

    Raises:
        401: Unauthorized - если пользователь не аутентифицирован
    """
    result = await db.execute(
        select(User)
        .where(User.id == current_user.id)
        .options(
            selectinload(User.followers),
            selectinload(User.following)
        )
    )
    user = result.scalar_one()

    return UserResponse(user=user)


@router.get("/{id}", response_model=UserResponse)
async def get_user_profile(
    id: int,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Получить профиль пользователя по ID.

    Args:
        id: ID запрашиваемого пользователя
        db: Асинхронная сессия БД

    Returns:
        UserResponse: Полная информация о пользователе включая:
            - Основные данные
            - Список подписчиков
            - Список подписок

    Raises:
        404: Not Found - если пользователь не найден
            Формат ошибки:
            {
                "result": False,
                "error_type": "not_found",
                "error_message": "User not found"
            }
    """
    result = await db.execute(
        select(User)
        .where(User.id == id)
        .options(
            selectinload(User.followers),
            selectinload(User.following)
        )
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "result": False,
                "error_type": "not_found",
                "error_message": "User not found"
            }
        )

    return UserResponse(user=user)
