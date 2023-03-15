from pydantic import BaseModel


class CategoryProduct(BaseModel):
    product_id: int
    category_id: int


class CategoryProductDetail(BaseModel):
    product_id: int
    category_id: int
    product_name: str
    product_description: str
    product_enable: bool
    category_name: str
    category_enable: bool
