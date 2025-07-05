"""
Модуль `schemas` определяет структуры данных:
- tweet.py: схемы для твитов
- user.py: схемы для пользователей и профилей
"""


from .user import UserProfile, UserResponse
from .tweet import TweetCreate


__all__ = ["UserProfile", "UserResponse", "TweetCreate"]
