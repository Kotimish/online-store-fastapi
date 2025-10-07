from abc import ABC, abstractmethod

from src.app.interfaces.repositories.base_repository import IRepository
from src.app.models.product import Product


class IProductRepository(IRepository[Product], ABC):
    """Интерфейс репозитория для товаров"""
    @abstractmethod
    async def get_by_category(self, category_id: int) -> list[Product]:
        """Получить список товаров из указанной категории"""
        raise NotImplementedError
