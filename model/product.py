from sqlalchemy import Boolean, Column, Integer, String

from db import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    enable = Column(Boolean, nullable=False)
