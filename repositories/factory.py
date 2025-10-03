from settings import settings, RepositoryType
from interfaces.repositories.category_repository import ICategoryRepository
from interfaces.repositories.product_repository import IProductRepository


def create_product_repository() -> IProductRepository:
    """Фабрика создания репозитория для товаров"""
    if settings.repository_type == RepositoryType.IN_MEMORY:
        from repositories.in_memory.product_repository import InMemoryProductRepository
        return InMemoryProductRepository()
    elif settings.repository_type == RepositoryType.JSON:
        from repositories.json.product_repository import JSONProductRepository
        return JSONProductRepository()
    else:
        raise ValueError(f"Unsupported storage type: {settings.storage_type}")


def create_category_repository() -> ICategoryRepository:
    """Фабрика создания репозитория для категорий товаров"""
    if settings.repository_type == RepositoryType.IN_MEMORY:
        from repositories.in_memory.category_repository import InMemoryCategoryRepository
        return InMemoryCategoryRepository()
    elif settings.repository_type == RepositoryType.JSON:
        from repositories.json.category_repository import JSONCategoryRepository
        return JSONCategoryRepository()
    else:
        raise ValueError(f"Unsupported storage type: {settings.storage_type}")
