from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class Product(BaseModel):
    """Model for products."""

    __tablename__ = 'products'

    name = Column(String(100), nullable=False, index=True)

    description = Column(Text, nullable=True)

    price = Column(Float, nullable=False)

    sku = Column(String(50), unique=True, nullable=False)

    # Foreign key ke tabel categories (relasi N:1).
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    is_active = Column(Boolean, default=True)

    # Setiap produk dimiliki oleh satu kategori.
    category = relationship('Category', back_populates='products')

    def __repr__(self):
        return f"<Product(name='{self.name}', sku='{self.sku}')>"
