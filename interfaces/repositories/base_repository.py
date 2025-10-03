from abc import ABC, abstractmethod
from typing import Generic

from pydantic import BaseModel
from typing_extensions import TypeVar

T = TypeVar('T', bound=BaseModel)


class IRepository(ABC, Generic[T]):
    """Интерфейс репозитория для категорий товаров"""

    @abstractmethod
    async def create(self, model: T) -> T:
        """Создать новую категорию товаров"""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, idx: int) -> T:
        """Получить категорию товаров по id"""
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[T]:
        """Получить список всех доступных категорий товаров"""
        raise NotImplementedError

    @abstractmethod
    async def update(self, idx: int, model: T) -> T:
        """Обновление указанной категории товаров"""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, idx: int) -> T:
        """
        Удаление категории из репозитория.
        Возвращает True, если удалено, иначе False.
        """
        raise NotImplementedError
