import asyncio

from src.app.interfaces.repositories.product_repository import IProductRepository
from src.app.models.product import Product


class InMemoryProductRepository(IProductRepository):
    """Репозитория для товаров с хранением в памяти приложения"""

    def __init__(self):
        self._storage: dict[int, Product] = {}
        self._lock = asyncio.Lock()

    def _get_next_id(self) -> int:
        if not self._storage:
            return 1
        valid_ids = [
            product.id
            for product in self._storage.values()
            if product.id is not None
        ]
        return max(valid_ids, default=-1) + 1

    async def create(self, product: Product) -> Product | None:
        async with self._lock:
            product_id = product.id
            if product_id is None:
                product_id = self._get_next_id()
                product.id = product_id
            elif product_id in self._storage:
                return None
            self._storage[product_id] = product
            return product

    async def get_by_id(self, product_id: int) -> Product | None:
        async with self._lock:
            return self._storage.get(product_id)

    async def get_all(self) -> list[Product]:
        async with self._lock:
            return list(self._storage.values())

    async def update(self, product_id: int, product: Product) -> Product | None:
        async with self._lock:
            if product_id not in self._storage:
                return None
            product.id = product_id
            self._storage[product_id] = product
            return product

    async def delete(self, product_id: int) -> Product | None:
        async with self._lock:
            if product_id not in self._storage:
                return None
            product = self._storage.pop(product_id)
            return product

    async def get_by_category(self, category_id: int) -> list[Product]:
        async with self._lock:
            return [
                product
                for product in self._storage.values()
                if product.category_id == category_id
            ]
