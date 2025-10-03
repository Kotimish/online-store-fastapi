from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from interfaces.repositories.category_repository import ICategoryRepository
from interfaces.repositories.product_repository import IProductRepository
from models.category import Category
from models.product import Product
from repositories import factory

router = APIRouter(prefix='/catalog', tags=['catalog'])
templates = Jinja2Templates(directory='templates')

CATEGORIES = [
    Category(
        id=1,
        name="Процессоры",
        slug="cpu",
        description=""
    ),
    Category(
        id=2,
        name="Видеокарты",
        slug="gpu",
        description=""
    ),
    Category(
        id=3,
        name="Оперативная память",
        slug="ram",
        description=""
    ),
    Category(
        id=4,
        name="SSD-накопители",
        slug="ssd",
        description=""
    )
]

PRODUCTS = [
    Product(
        id=1,
        name="AFox GeForce RTX 3060 12GB DUAL",
        price=23990.00,
        category_id=2,
        description=(
            "Видеокарта AFOX GeForce RTX 3060 [AF3060-12GD6H2] – отличный выбор для пользователей,"
            " которые хотят собрать или модернизировать игровой компьютер высокого класса."
            " Устройство, оснащенное широко распространенным графическим процессором GeForce RTX 3060,"
            " обеспечивает комфортное восприятие графики подавляющего большинства видеоигр."
            " Потенциал видеопроцессора полностью раскрывается благодаря большому (12 ГБ) объему видеопамяти. "
        )
    )
]


@router.get("/", response_class=HTMLResponse)
async def get_catalog_page(
        request: Request,
        repository: ICategoryRepository = Depends(factory.create_category_repository)
):
    """Страница с каталогом товаров"""
    categories: list[Category] = await repository.get_all()
    context = {
        "request": request,
        "categories": categories,
    }
    return templates.TemplateResponse(
        "catalog.html",
        context
    )


@router.get("/{category_slug}", response_class=HTMLResponse)
async def get_category_page(
        request: Request,
        category_slug: str,
        product_repository: IProductRepository = Depends(factory.create_product_repository),
        category_repository: ICategoryRepository = Depends(factory.create_category_repository)
):
    """Страница с каталогом товаров категории"""
    category_products: list[Product] = []
    products: list[Product] = await product_repository.get_all()
    category: Category = await category_repository.get_by_slug(category_slug)
    for product in products:
        if product.category_id == category.id:
            category_products.append(product)
    context = {
        "request": request,
        "category": category.name,
        "products": category_products,
    }
    return templates.TemplateResponse(
        "catalog_category.html",
        context
    )
