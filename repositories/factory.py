from interfaces.repositories.category_repository import ICategoryRepository
from interfaces.repositories.product_repository import IProductRepository
from settings import settings, RepositoryType

_product_repository: IProductRepository | None = None
_category_repository: ICategoryRepository | None = None


def create_product_repository() -> IProductRepository:
    """Фабрика создания репозитория для товаров"""
    global _product_repository
    if _product_repository is None:
        if settings.repository_type == RepositoryType.IN_MEMORY:
            from repositories.in_memory.product_repository import InMemoryProductRepository
            _product_repository = InMemoryProductRepository()
        elif settings.repository_type == RepositoryType.JSON:
            from repositories.json.product_repository import JSONProductRepository
            _product_repository = JSONProductRepository()
        else:
            raise ValueError(f"Unsupported storage type: {settings.storage_type}")
    return _product_repository


def create_category_repository() -> ICategoryRepository:
    """Фабрика создания репозитория для категорий товаров"""
    global _category_repository
    if _category_repository is None:
        if settings.repository_type == RepositoryType.IN_MEMORY:
            from repositories.in_memory.category_repository import InMemoryCategoryRepository
            _category_repository = InMemoryCategoryRepository()
        elif settings.repository_type == RepositoryType.JSON:
            from repositories.json.category_repository import JSONCategoryRepository
            _category_repository = JSONCategoryRepository()
        else:
            raise ValueError(f"Unsupported storage type: {settings.storage_type}")
    return _category_repository
