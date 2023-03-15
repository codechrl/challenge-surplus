from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db import Base


class ProductImage(Base):
    __tablename__ = "product_image"

    product_id = Column(
        Integer, ForeignKey("product.id"), primary_key=True, nullable=False
    )
    image_id = Column(Integer, ForeignKey("image.id"), primary_key=True, nullable=False)
    image = relationship("Image", back_populates="products")
    product = relationship("Product", back_populates="images")
