from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import get_current_user
from sqlalchemy import insert, delete, select
from src.api.schemas.user import UserResponse
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from src.db.models import User, Follow
from src.db.database import get_db


router = APIRouter()


@router.post("/{id}/follow")
async def follow_user(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
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
):
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
):
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
):
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
