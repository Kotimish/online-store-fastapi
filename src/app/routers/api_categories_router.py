from fastapi import APIRouter, Depends, HTTPException

from src.app.interfaces.repositories.category_repository import ICategoryRepository
from src.app.models.category import Category
from src.app.repositories import factory

router = APIRouter(prefix='/api/category', tags=['api_category'])


@router.get("/", response_model=list[Category])
async def get_categories(
        # category_id: int = Query(None, description="Product category"),
        repository: ICategoryRepository = Depends(factory.create_category_repository),
):
    """Получить список Категорий"""
    categories = await repository.get_all()
    return categories


@router.get("/{category_id}", response_model=Category)
async def get_category_by_id(
        category_id: int,
        repository: ICategoryRepository = Depends(factory.create_category_repository),
):
    """Получить информацию по Категории"""
    category = await repository.get_by_id(category_id)
    if category is None:
        raise HTTPException(
            status_code=404,
            detail=f"Category with id {category_id} not found"
        )
    return category


@router.post("/", response_model=Category, status_code=201)
async def create_category(
        new_category: Category,
        repository: ICategoryRepository = Depends(factory.create_category_repository),
):
    """Добавить новую Категорию"""
    category = await repository.create(new_category)
    if category is None:
        raise HTTPException(
            status_code=409,
            detail=f"Category with id {new_category.id} already exists"
        )
    return category


@router.put("/{category_id}")
async def edit_category(
        category_id: int,
        product: Category,
        repository: ICategoryRepository = Depends(factory.create_category_repository),
):
    """Обновить Категорию"""
    category = await repository.update(category_id, product)
    if category is None:
        raise HTTPException(
            status_code=404,
            detail=f"Category with id {category_id} not found"
        )
    return category


@router.delete("/{category_id}")
async def delete_category(
        category_id: int,
        repository: ICategoryRepository = Depends(factory.create_category_repository),
):
    """Удалить Категорию"""
    category = await repository.delete(category_id)
    if category is None:
        raise HTTPException(
            status_code=404,
            detail=f"Category with id {category_id} not found"
        )
    return category
