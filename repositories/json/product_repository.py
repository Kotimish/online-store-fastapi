from pathlib import Path

import settings
from interfaces.repositories.product_repository import IProductRepository
from models.product import Product
from repositories.json.json_repository import JSONRepository


class JSONProductRepository(IProductRepository):
    """Репозитория для товаров с хранением в памяти приложения"""

    def __init__(self, file_path: Path | None = None):
        self.file_path: Path = file_path or settings.BASE_DIR / "data" / "products.json"
        self._storage: JSONRepository = JSONRepository(self.file_path)

    async def get_next_id(self):
        products = await self.get_all()
        last_product = max(products, key=lambda product: product.id)
        return last_product.id + 1

    async def create(self, new_product: Product) -> Product:
        products = await self.get_all()
        new_product.id = await self.get_next_id()
        products.append(new_product)
        self._storage.save([
            product.model_dump()
            for product in products
        ])
        return new_product

    async def get_by_id(self, idx: int) -> Product:
        products = await self.get_all()
        return next(
            (
                product
                for product in products
                if product.id == idx
            ),
            None
        )

    async def get_all(self) -> list[Product]:
        data = self._storage.load()
        return [Product(**item) for item in data]

    async def update(self, idx: int, new_product: Product) -> Product | None:
        products = await self.get_all()
        for number, product in enumerate(products):
            if product.id == idx:
                new_product.id = product.id
                products[number] = new_product
                self._storage.save([
                    product.model_dump()
                    for product in products]
                )
                return new_product
        return None

    async def delete(self, idx: int) -> Product:
        products = await self.get_all()
        saved_products = []
        deleted_products = []
        for product in products:
            if product.id == idx:
                deleted_products.append(product)
            else:
                saved_products.append(product)
        self._storage.save([
            product.model_dump()
            for product in saved_products]
        )
        return next(
            (product for product in deleted_products),
            None
        )

    async def get_by_category(self, category_id: int) -> list[Product]:
        products = await self.get_all()
        return [
            product
            for product in products
            if product.category_id == category_id
        ]
