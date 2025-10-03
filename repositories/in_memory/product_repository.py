from interfaces.repositories.product_repository import IProductRepository
from models.category import Category
from models.product import Product


class InMemoryProductRepository(IProductRepository):
    """Репозитория для товаров с хранением в памяти приложения"""
    def __init__(self):
        self._storage: dict[int, Product] = {}
        self._count: int = 0

    async def create(self, model: Product) -> Product:
        model.id = self._count
        self._storage[self._count] = model
        self._count+= 1
        return model

    async def get_by_id(self, idx: int) -> Product:
        return self._storage.get(idx)

    async def get_all(self) -> list[Product]:
        return list(self._storage.values())

    async def update(self, idx: int, model: Product) -> Product:
        model.id = idx
        self._storage[idx] = model
        return model

    async def delete(self, idx: int) -> Product:
        model = self._storage.pop(idx)
        return model

    async def get_by_category(self, category_id: int) -> list[Product]:
        return [
            product
            for product in self._storage.values()
            if product.category_id == category_id
        ]
