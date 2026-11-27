from typing import List, Optional

from sqlalchemy import select

from ..models.category import Category


class CategoryService:
    """Service for category operations."""

    @staticmethod
    def get_all_categories(dbsession) -> List[Category]:
        """Get all active categories."""
        return dbsession.execute(
            select(Category)
            .where(Category.is_active == True)  # noqa: E712
            .order_by(Category.id)
        ).scalars().all()

    @staticmethod
    def get_category_by_id(dbsession, category_id: int) -> Optional[Category]:
        """Get category by ID."""
        return dbsession.get(Category, category_id)

    @staticmethod
    def get_category_by_name(dbsession, name: str) -> Optional[Category]:
        """Get category by name."""
        return dbsession.execute(
            select(Category).where(Category.name == name)
        ).scalar_one_or_none()

    @staticmethod
    def create_category(dbsession, category_data: dict) -> Category:
        """Create a new category."""
        category = Category(**category_data)
        dbsession.add(category)
        dbsession.flush()
        return category

    @staticmethod
    def update_category(dbsession, category: Category, update_data: dict) -> Category:
        """Update existing category."""
        for field, value in update_data.items():
            setattr(category, field, value)
        dbsession.add(category)
        dbsession.flush()
        return category

    @staticmethod
    def delete_category(dbsession, category: Category) -> None:
        """Soft delete a category."""
        category.is_active = False
        dbsession.add(category)
        dbsession.flush()
