from fastapi import APIRouter, Depends, Query, HTTPException

from src.app.interfaces.repositories.product_repository import IProductRepository
from src.app.models.product import Product
from src.app.repositories import factory

router = APIRouter(prefix='/api/product', tags=['api_product'])


@router.get("/", response_model=list[Product])
async def get_products(
        category_id: int = Query(None, description="Product category"),
        repository: IProductRepository = Depends(factory.create_product_repository),
):
    """Получить список товаров"""
    products = await repository.get_all()
    if category_id is not None:
        products = [
            product
            for product in products
            if product.category_id == category_id
        ]
    return products


@router.get("/{product_id}", response_model=Product)
async def get_product_by_id(
        product_id: int,
        repository: IProductRepository = Depends(factory.create_product_repository),
):
    """Получить информацию по товару"""
    product = await repository.get_by_id(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} not found"
        )
    return product


@router.post("/", response_model=Product, status_code=201)
async def create_product(
        new_product: Product,
        repository: IProductRepository = Depends(factory.create_product_repository),
):
    """Добавить новый товар"""
    product = await repository.create(new_product)
    if product is None:
        raise HTTPException(
            status_code=409,
            detail=f"Product with id {new_product.id} already exists"
        )
    return product


@router.put("/{product_id}")
async def edit_product(
        product_id: int,
        product: Product,
        repository: IProductRepository = Depends(factory.create_product_repository),
):
    """Обновить товар"""
    product = await repository.update(product_id, product)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} not found"
        )
    return product


@router.delete("/{product_id}")
async def delete_product(
        product_id: int,
        repository: IProductRepository = Depends(factory.create_product_repository),
):
    """Удалить товар"""
    product = await repository.delete(product_id)
    if product is None:
        raise HTTPException(
            status_code=404,
            detail=f"Product with id {product_id} not found"
        )
    return product
