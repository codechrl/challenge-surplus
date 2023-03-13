from fastapi import HTTPException
from pydantic import BaseModel


class BasicMessage(BaseModel):
    message: str


class Pagination(BaseModel):
    page: int
    limit: int
    total: int


class Response(BaseModel):
    status: str
    code: int
    message: str = None
    data: list[dict] = None
    pagination: Pagination = None


class ResponseHTTPException(HTTPException):
    def __init__(self, message):
        super().__init__(status="error", code=500, message=message)
