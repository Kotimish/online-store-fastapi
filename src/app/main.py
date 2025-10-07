import uvicorn
from fastapi import FastAPI

from src.app.routers.api_categories_router import router as api_categories_router
from src.app.routers.api_products_router import router as api_products_router
from src.app.routers.catalog_router import router as catalog_router
from src.app.routers.main_pages_router import router as main_pages_router

app = FastAPI()
app.include_router(main_pages_router)
app.include_router(api_products_router)
app.include_router(api_categories_router)
app.include_router(catalog_router)


def run():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    run()
