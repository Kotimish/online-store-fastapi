from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=['main'])

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Главная страница сайта"""
    context = {
        "request": request,
    }
    return templates.TemplateResponse(
        "index.html",
        context
    )


@router.get("/about/", response_class=HTMLResponse)
def about(request: Request):
    """Страница с информацией о сайте"""
    context = {
        "request": request,
        "contact_phone": "+7 **********",
        "email": "info@example.com",
    }
    return templates.TemplateResponse(
        "about.html",
        context
    )


@router.get("/catalog/", response_class=HTMLResponse)
def catalog(request: Request):
    """Страница с каталогом товаров"""
    context = {
        "request": request,
    }
    return templates.TemplateResponse(
        "catalog.html",
        context
    )


@router.get("/delivery/", response_class=HTMLResponse)
def delivery(request: Request):
    """Страница с информацией о доставке"""
    context = {
        "request": request,
    }
    return templates.TemplateResponse(
        "delivery.html",
        context
    )


@router.get("/how-buy/", response_class=HTMLResponse)
def how_buy(request: Request):
    """Страница с информацией о покупке"""
    context = {
        "request": request,
    }
    return templates.TemplateResponse(
        "how-buy.html",
        context
    )
