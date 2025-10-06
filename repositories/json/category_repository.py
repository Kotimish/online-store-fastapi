import asyncio
from pathlib import Path

import settings
from interfaces.repositories.category_repository import ICategoryRepository
from models.category import Category
from repositories.json.json_repository import JSONRepository


class JSONCategoryRepository(ICategoryRepository):
    """Репозитория для категорий с хранением в JSON-файле"""

    def __init__(self, file_path: Path | None = None):
        self.file_path: Path = file_path or settings.BASE_DIR / "data" / "categories.json"
        self._storage: JSONRepository = JSONRepository(self.file_path)
        self._lock = asyncio.Lock()

    async def _save_categories(self, categories: list[Category]) -> None:
        data = [
            category.model_dump()
            for category in categories
        ]
        await asyncio.to_thread(self._storage.save, data)

    async def _load_categories(self) -> list[Category]:
        data = await asyncio.to_thread(self._storage.load)
        return [Category.model_validate(item) for item in data]

    async def create(self, new_category: Category) -> Category | None:
        async with self._lock:
            categories = await self._load_categories()
            valid_ids = [
                category.id
                for category in categories
                if category.id is not None
            ]
            if new_category.id is None:
                new_category.id = max(valid_ids, default=-1) + 1
            elif new_category.id in valid_ids:
                return None
            categories.append(new_category)
            await self._save_categories(categories)
            return new_category

    async def get_by_id(self, idx: int) -> Category | None:
        async with self._lock:
            categories = await self._load_categories()
            return next(
                (
                    category
                    for category in categories
                    if category.id == idx
                ),
                None
            )

    async def get_all(self) -> list[Category]:
        async with self._lock:
            return await self._load_categories()

    async def update(self, idx: int, new_category: Category) -> Category | None:
        async with self._lock:
            categories = await self._load_categories()
            for number, category in enumerate(categories):
                if category.id == idx:
                    new_category.id = category.id
                    categories[number] = new_category
                    await self._save_categories(categories)
                    return new_category
            return None

    async def delete(self, idx: int) -> Category | None:
        async with self._lock:
            categories = await self._load_categories()
            saved_categories = []
            deleted_category = None
            deleted_count = 0
            for category in categories:
                if category.id == idx:
                    deleted_category = category
                    deleted_count += 1
                else:
                    saved_categories.append(category)
            await self._save_categories(saved_categories)

            if deleted_count > 1:
                # todo добавить лог, что было найдено несколько объектов с одним id
                pass
            return deleted_category

    async def get_by_slug(self, slug: str) -> Category | None:
        async with self._lock:
            categories = await self._load_categories()
            return next(
                (
                    category
                    for category in categories
                    if category.slug == slug
                ),
                None
            )
