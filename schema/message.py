from typing import List, TypeVar, Union

from pydantic import BaseModel

from schema.category import Category
from schema.category_product import CategoryProductDetail
from schema.image import Image
from schema.product import Product

T = TypeVar("T")


class ValidationError(BaseModel):
    loc: list = None
    msg: str = None
    type: str = None


class BasicMessage(BaseModel):
    message: str


class IdMessage(BaseModel):
    id: int


class CategoryProductIdMessage(BaseModel):
    product_id: int
    category_id: int


class Pagination(BaseModel):
    page: int
    limit: int
    total_page: int
    total_all: int


class Response(BaseModel):
    status: str = "success"
    code: int = 200
    message: Union[dict, str, List[ValidationError]] = None
    data: Union[List[T], IdMessage, CategoryProductIdMessage] = None
    pagination: Pagination = None


class ValidationErrorResponse(Response):
    message: List[ValidationError] = None


class IdResponse(Response):
    data: IdMessage = None


class CategoryProductIdResponse(Response):
    data: CategoryProductIdMessage = None


class CategoriesResponse(Response):
    data: List[Category] = None


class ProductResponse(Response):
    data: List[Product] = None


class CategoryProductDetailResponse(Response):
    data: List[CategoryProductDetail] = None


class ImageResponse(Response):
    data: List[Image] = None
