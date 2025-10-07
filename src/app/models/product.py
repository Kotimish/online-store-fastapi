from typing import Optional

from pydantic import BaseModel


class Product(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    category_id: int  # "cpu", "gpu", "ram", "ssd", ...
    description: Optional[str] = None
