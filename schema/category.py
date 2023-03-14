from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str
    enable: bool


class CategoryPost(BaseModel):
    name: str
    enable: bool


class CategoryPut(BaseModel):
    name: str = None
    enable: bool = None
