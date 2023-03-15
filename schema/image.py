from pydantic import BaseModel


class Image(BaseModel):
    id: int
    name: str
    file: str
    enable: bool


class ImagePost(BaseModel):
    name: str
    enable: bool


class ImagePut(BaseModel):
    name: str = None
    enable: bool = None
