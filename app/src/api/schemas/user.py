from pydantic import BaseModel, ConfigDict
from typing import List


class FollowerInfo(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class FollowingInfo(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class UserProfile(BaseModel):
    id: int
    name: str
    followers: List[FollowerInfo] = []
    following: List[FollowingInfo] = []
    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseModel):
    result: bool = True
    user: UserProfile
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "result": True,
                "user": {
                    "id": 1,
                    "name": "Иван Иванов",
                    "followers": [{"id": 2, "name": "Петр Петров"}],
                    "following": [{"id": 3, "name": "Сидор Сидоров"}]
                }
            }
        }
    )
