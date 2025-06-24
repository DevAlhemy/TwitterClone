from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_db, User


async def get_current_user(
    api_key: str = Header(...),
    db: AsyncSession = Depends(get_db)
) -> User:
    result = await db.execute(select(User).where(User.api_key == api_key))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return user
