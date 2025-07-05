from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from core.security import get_current_user, get_db, User
from sqlalchemy.ext.asyncio import AsyncSession
from db import Media
import shutil
import uuid
import os


router = APIRouter()

UPLOAD_DIR = "media"


@router.post("", status_code=201)
async def upload_media(
        file: UploadFile = File(...),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> dict:
    """
    Загружает изображение на сервер.

    Args:
        file: Загружаемый файл (разрешены: .jpg, .jpeg, .png, .gif, до 10MB)
        db: Сессия БД
        current_user: Текущий пользователь

    Returns:
        {"result": bool, "media_id": int}

    Raises:
        400: Неподдерживаемый тип файла или превышен размер
        401: Пользователь не аутентифицирован
        500: Ошибка сохранения файла
    """

    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}

    file_ext = os.path.splitext(file.filename)[-1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Unsupported file type")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = f"{UPLOAD_DIR}/{file_name}"

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except IOError as e:
        raise HTTPException(500, f"Failed to save file: {str(e)}")

    new_media = Media(file_path=file_name)
    db.add(new_media)
    await db.commit()
    await db.refresh(new_media)

    return {"result": True, "media_id": new_media.id}
