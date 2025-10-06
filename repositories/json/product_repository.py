import asyncio
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
        self._lock = asyncio.Lock()

    async def _save_products(self, products: list[Product]):
        data = [
            product.model_dump()
            for product in products
        ]
        await asyncio.to_thread(self._storage.save, data)

    async def _load_products(self) -> list[Product]:
        data = await asyncio.to_thread(self._storage.load)
        return [Product.model_validate(item) for item in data]

    async def create(self, new_product: Product) -> Product | None:
        async with self._lock:
            products = await self._load_products()
            valid_ids = [
                product.id
                for product in products
                if product.id is not None
            ]
            if new_product.id is None:
                new_product.id =  max(valid_ids, default=-1) + 1
            elif new_product.id in valid_ids:
                return None
            products.append(new_product)
            await self._save_products(products)
            return new_product

    async def get_by_id(self, idx: int) -> Product | None:
        async with self._lock:
            products = await self._load_products()
            return next(
                (
                    product
                    for product in products
                    if product.id == idx
                ),
                None
            )

    async def get_all(self) -> list[Product]:
        async with self._lock:
            return await self._load_products()

    async def update(self, idx: int, new_product: Product) -> Product | None:
        async with self._lock:
            products = await self._load_products()
            for number, product in enumerate(products):
                if product.id == idx:
                    new_product.id = product.id
                    products[number] = new_product
                    await self._save_products(products)
                    return new_product
            return None

    async def delete(self, idx: int) -> Product | None:
        async with self._lock:
            products = await self._load_products()
            saved_products = []
            deleted_product = None
            deleted_count = 0
            for product in products:
                if product.id == idx:
                    deleted_product = product
                    deleted_count += 1
                else:
                    saved_products.append(product)
            await self._save_products(saved_products)

            if deleted_count > 1:
                # todo добавить лог, что было найдено несколько объектов с одним id
                pass
            return deleted_product

    async def get_by_category(self, category_id: int) -> list[Product]:
        async with self._lock:
            products = await self._load_products()
            return [
                product
                for product in products
                if product.category_id == category_id
            ]
