import asyncio

from src.app.interfaces.repositories.category_repository import ICategoryRepository
from src.app.models.category import Category


class InMemoryCategoryRepository(ICategoryRepository):
    """Репозитория для категорий с хранением в памяти приложения"""
    def __init__(self):
        self._storage: dict[int, Category] = {}
        self._lock = asyncio.Lock()

    def _get_next_id(self) -> int:
        if not self._storage:
            return 1
        valid_ids = [
            category.id
            for category in self._storage.values()
            if category.id is not None
        ]
        return max(valid_ids, default=-1) + 1

    async def create(self, category: Category) -> Category | None:
        async with self._lock:
            category_id = category.id
            if category_id is None:
                category_id = self._get_next_id()
                category.id = category_id
            elif category_id in self._storage:
                return None
            self._storage[category_id] = category
            return category

    async def get_by_id(self, category_id: int) -> Category | None:
        async with self._lock:
            return self._storage.get(category_id)

    async def get_all(self) -> list[Category]:
        async with self._lock:
            return list(self._storage.values())

    async def update(self, category_id: int, category: Category) -> Category | None:
        async with self._lock:
            if category_id not in self._storage:
                return None
            category.id = category_id
            self._storage[category_id] = category
            return category

    async def delete(self, category_id: int) -> Category | None:
        async with self._lock:
            if category_id not in self._storage:
                return None
            category = self._storage.pop(category_id)
            return category

    async def get_by_slug(self, slug: str) -> Category | None:
        async with self._lock:
            for category in self._storage.values():
                if category.slug == slug:
                    return category
            return None
