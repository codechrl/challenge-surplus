from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    description: str
    enable: bool


class ProductPost(BaseModel):
    name: str
    description: str
    enable: bool


class ProductPut(BaseModel):
    name: str = None
    description: str = None
    enable: bool = None
