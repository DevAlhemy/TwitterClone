from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from .user import UserProfile
from datetime import datetime


class LikeInfo(BaseModel):
    user_id: int
    name: str


class TweetCreate(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = None


class TweetOut(BaseModel):
    id: int
    content: str
    created_at: datetime
    author: UserProfile
    model_config = ConfigDict(from_attributes=True)


class TweetFeedOut(BaseModel):
    id: int
    content: str
    author: UserProfile
    likes: List[LikeInfo]
    attachments: List[str]
    model_config = ConfigDict(from_attributes=True)
