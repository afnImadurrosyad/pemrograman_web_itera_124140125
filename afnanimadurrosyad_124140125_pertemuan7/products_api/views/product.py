from marshmallow import ValidationError
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPNoContent, HTTPNotFound

from ..services.category import CategoryService
from ..services.product import ProductService
from ..schemas.product import (
    ProductCreateSchema,
    ProductSchema,
    ProductUpdateSchema,
)


@view_config(route_name='api_v1.products', request_method='GET', renderer='json')
def get_products(request):
    """Get all active products."""
    products = ProductService.get_all_products(request.dbsession)
    schema = ProductSchema(many=True)
    return schema.dump(products)


@view_config(route_name='api_v1.products', request_method='POST', renderer='json')
def create_product(request):
    """Create a new product."""
    try:
        payload = request.json_body
    except ValueError:
        raise HTTPBadRequest(json={'errors': {'body': ['Invalid JSON payload']}})

    schema = ProductCreateSchema()
    try:
        product_data = schema.load(payload)
    except ValidationError as err:
        raise HTTPBadRequest(json={'errors': err.messages})

    # Check if SKU already exists
    if ProductService.get_product_by_sku(request.dbsession, product_data['sku']):
        raise HTTPBadRequest(
            json={'errors': {'sku': ['Product with this SKU already exists']}}
        )

    # Check if the referenced category exists and is active
    category = CategoryService.get_category_by_id(
        request.dbsession, product_data['category_id']
    )
    if not category or not category.is_active:
        raise HTTPBadRequest(
            json={'errors': {'category_id': ['Category does not exist']}}
        )

    product = ProductService.create_product(request.dbsession, product_data)
    request.response.status = 201
    return ProductSchema().dump(product)


@view_config(route_name='api_v1.product', request_method='GET', renderer='json')
def get_product(request):
    """Get product by ID."""
    product_id = int(request.matchdict['id'])
    product = ProductService.get_product_by_id(request.dbsession, product_id)
    if not product or not product.is_active:
        raise HTTPNotFound()
    return ProductSchema().dump(product)


@view_config(route_name='api_v1.product', request_method='PUT', renderer='json')
def update_product(request):
    """Update existing product."""
    product_id = int(request.matchdict['id'])
    product = ProductService.get_product_by_id(request.dbsession, product_id)
    if not product or not product.is_active:
        raise HTTPNotFound()

    try:
        payload = request.json_body
    except ValueError:
        raise HTTPBadRequest(json={'errors': {'body': ['Invalid JSON payload']}})

    schema = ProductUpdateSchema()
    try:
        update_data = schema.load(payload)
    except ValidationError as err:
        raise HTTPBadRequest(json={'errors': err.messages})

    # Check if the new category (if changed) exists and is active
    new_category_id = update_data.get('category_id')
    if new_category_id is not None and new_category_id != product.category_id:
        category = CategoryService.get_category_by_id(request.dbsession, new_category_id)
        if not category or not category.is_active:
            raise HTTPBadRequest(
                json={'errors': {'category_id': ['Category does not exist']}}
            )

    updated_product = ProductService.update_product(
        request.dbsession, product, update_data
    )
    return ProductSchema().dump(updated_product)


@view_config(route_name='api_v1.product', request_method='DELETE')
def delete_product(request):
    """Soft delete a product."""
    product_id = int(request.matchdict['id'])
    product = ProductService.get_product_by_id(request.dbsession, product_id)
    if not product or not product.is_active:
        raise HTTPNotFound()
    ProductService.delete_product(request.dbsession, product)
    return HTTPNoContent()
