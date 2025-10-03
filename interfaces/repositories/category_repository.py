from abc import ABC, abstractmethod

from interfaces.repositories.base_repository import IRepository
from models.category import Category


class ICategoryRepository(IRepository[Category], ABC):
    """Интерфейс репозитория для категорий товаров"""
    @abstractmethod
    async def get_by_slug(self, slug: str) -> Category | None:
        """Получить категорию по указателю"""
        raise NotImplementedError
