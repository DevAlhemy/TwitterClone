from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_db, User


async def get_current_user(
    api_key: str = Header(...),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Получает текущего пользователя по API-ключу из заголовков.

    Args:
        api_key: Ключ API, передаваемый в заголовке запроса
        db: Асинхронная сессия базы данных

    Returns:
        User: Объект аутентифицированного пользователя

    Raises:
        HTTPException: 401 Unauthorized - если:
            - API-ключ не передан
            - Пользователь с таким ключом не найден
    """
    result = await db.execute(select(User).where(User.api_key == api_key))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    return user
