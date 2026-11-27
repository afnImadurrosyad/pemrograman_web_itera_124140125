# Import views to register them
from .category import (
    get_categories,
    create_category,
    get_category,
    update_category,
    delete_category,
)
from .cors import cors_options_view
from .default import home, notfound
from .product import (
    get_products,
    create_product,
    get_product,
    update_product,
    delete_product,
)

__all__ = [
    'get_categories',
    'create_category',
    'get_category',
    'update_category',
    'delete_category',
    'cors_options_view',
    'home',
    'notfound',
    'get_products',
    'create_product',
    'get_product',
    'update_product',
    'delete_product',
]
