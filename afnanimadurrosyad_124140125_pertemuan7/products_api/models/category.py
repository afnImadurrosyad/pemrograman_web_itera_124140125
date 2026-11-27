from sqlalchemy import Boolean, Column, String, Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class Category(BaseModel):
    """Model for product categories."""

    __tablename__ = 'categories'

    name = Column(String(100), unique=True, nullable=False, index=True)

    description = Column(Text, nullable=True)

    is_active = Column(Boolean, default=True)

    # Satu kategori memiliki banyak produk (relasi 1:N).
    products = relationship('Product', back_populates='category')

    @property
    def active_products(self):
        """Produk aktif milik kategori ini (soft-deleted tidak ikut)."""
        return [product for product in self.products if product.is_active]

    def __repr__(self):
        return f"<Category(name='{self.name}')>"
