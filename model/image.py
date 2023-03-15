from sqlalchemy import Boolean, Column, Integer, String

from db import Base


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)
    file = Column(String, nullable=False)
    enable = Column(Boolean, nullable=False)
