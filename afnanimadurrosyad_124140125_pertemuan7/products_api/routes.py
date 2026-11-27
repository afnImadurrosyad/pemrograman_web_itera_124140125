"""Peta URL Dispatch (routing REST API) aplikasi."""


def includeme(config):
    """Configure routes."""
    config.add_route('home', '/')

    # REST API Categories
    config.add_route('api_v1.categories', '/api/v1/categories')
    config.add_route('api_v1.category', r'/api/v1/categories/{id:\d+}')

    # REST API Products
    config.add_route('api_v1.products', '/api/v1/products')
    config.add_route('api_v1.product', r'/api/v1/products/{id:\d+}')
