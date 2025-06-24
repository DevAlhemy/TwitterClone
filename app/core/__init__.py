"""
Модуль `core` содержит:
- config.py: работа с переменными окружения
- security.py: аутентификация и зависимости безопасности
"""


from .config import settings, Settings, SettingsConfigDict
from .security import get_current_user


__all__ = ["settings", "get_current_user", "Settings", "SettingsConfigDict"]
