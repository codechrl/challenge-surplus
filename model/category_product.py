from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db import Base


class CategoryProduct(Base):
    __tablename__ = "category_product"

    product_id = Column(
        Integer, ForeignKey("product.id"), primary_key=True, nullable=False
    )
    category_id = Column(
        Integer, ForeignKey("category.id"), primary_key=True, nullable=False
    )
    category = relationship("Category", back_populates="products")
    product = relationship("Product", back_populates="categories")
