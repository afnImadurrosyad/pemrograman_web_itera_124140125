from typing import List, Optional

from sqlalchemy import select

from ..models.product import Product


class ProductService:
    """Service for product operations."""

    @staticmethod
    def get_all_products(dbsession) -> List[Product]:
        """Get all active products."""
        return dbsession.execute(
            select(Product)
            .where(Product.is_active == True)  # noqa: E712
            .order_by(Product.id)
        ).scalars().all()

    @staticmethod
    def get_product_by_id(dbsession, product_id: int) -> Optional[Product]:
        """Get product by ID."""
        return dbsession.get(Product, product_id)

    @staticmethod
    def get_product_by_sku(dbsession, sku: str) -> Optional[Product]:
        """Get product by SKU."""
        return dbsession.execute(
            select(Product).where(Product.sku == sku)
        ).scalar_one_or_none()

    @staticmethod
    def create_product(dbsession, product_data: dict) -> Product:
        """Create a new product."""
        product = Product(**product_data)
        dbsession.add(product)
        dbsession.flush()
        return product

    @staticmethod
    def update_product(dbsession, product: Product, update_data: dict) -> Product:
        """Update existing product."""
        for field, value in update_data.items():
            setattr(product, field, value)
        dbsession.add(product)
        dbsession.flush()
        return product

    @staticmethod
    def delete_product(dbsession, product: Product) -> None:
        """Soft delete a product."""
        product.is_active = False
        dbsession.add(product)
        dbsession.flush()
