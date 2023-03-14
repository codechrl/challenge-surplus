from sqlalchemy import Boolean, Column, Integer, MetaData, String

from db import Base

metadata = MetaData()


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    enable = Column(Boolean, nullable=False)
