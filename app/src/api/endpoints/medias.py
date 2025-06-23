from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import get_current_user
from src.db.models import Media, User
from src.db.database import get_db
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
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_ext = os.path.splitext(file.filename)[-1]
    file_name = f"{uuid.uuid4()}{file_ext}"
    file_path = f"{UPLOAD_DIR}/{file_name}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    new_media = Media(file_path=file_name)
    db.add(new_media)
    await db.commit()
    await db.refresh(new_media)

    return {"result": True, "media_id": new_media.id}
