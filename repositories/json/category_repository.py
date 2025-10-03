from pathlib import Path

import settings
from interfaces.repositories.category_repository import ICategoryRepository
from models.category import Category
from repositories.json.json_repository import JSONRepository


class JSONCategoryRepository(ICategoryRepository):
    """Репозитория для товаров с хранением в памяти приложения"""

    def __init__(self, file_path: Path | None = None):
        self.file_path: Path = file_path or settings.BASE_DIR / "data" / "categories.json"
        self._storage: JSONRepository = JSONRepository(self.file_path)

    async def get_next_id(self):
        categories = await self.get_all()
        last_category = max(categories, key=lambda category: category.id)
        return last_category.id + 1

    async def create(self, new_category: Category) -> Category:
        categories = await self.get_all()
        new_category.id = await self.get_next_id()
        categories.append(new_category)
        self._storage.save([
            category.model_dump()
            for category in categories
        ])
        return new_category

    async def get_by_id(self, idx: int) -> Category:
        categories = await self.get_all()
        return next(
            (
                category
                for category in categories
                if category.id == idx
            ),
            None
        )

    async def get_all(self) -> list[Category]:
        data = self._storage.load()
        return [Category(**item) for item in data]

    async def update(self, idx: int, new_category: Category) -> Category | None:
        categories = await self.get_all()
        for number, category in enumerate(categories):
            if category.id == idx:
                new_category.id = category.id
                categories[number] = new_category
                self._storage.save([
                    category.model_dump()
                    for category in categories]
                )
                return new_category
        return None

    async def delete(self, idx: int) -> Category:
        categories = await self.get_all()
        saved_categories = []
        deleted_categories = []
        for category in categories:
            if category.id == idx:
                deleted_categories.append(category)
            else:
                saved_categories.append(category)
        self._storage.save([
            category.model_dump()
            for category in saved_categories]
        )
        return next(
            (category for category in deleted_categories),
            None
        )

    async def get_by_slug(self, slug: str) -> Category | None:
        categories = await self.get_all()
        return next(
            (
                category
                for category in categories
                if category.slug == slug
            ),
            None
        )
