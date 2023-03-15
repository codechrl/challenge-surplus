from pydantic import BaseModel


class ProductImage(BaseModel):
    product_id: int
    image_id: int


class ProductImageDetail(BaseModel):
    product_id: int
    image_id: int
    product_name: str
    product_description: str
    product_enable: bool
    image_name: str
    image_file: str
    image_enable: bool
