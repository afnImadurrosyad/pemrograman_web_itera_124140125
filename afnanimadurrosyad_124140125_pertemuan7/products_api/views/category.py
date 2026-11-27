from marshmallow import ValidationError
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPNoContent, HTTPNotFound

from ..services.category import CategoryService
from ..schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)


@view_config(route_name='api_v1.categories', request_method='GET', renderer='json')
def get_categories(request):
    """Get all active categories."""
    categories = CategoryService.get_all_categories(request.dbsession)
    schema = CategorySchema(many=True)
    return schema.dump(categories)


@view_config(route_name='api_v1.categories', request_method='POST', renderer='json')
def create_category(request):
    """Create a new category."""
    try:
        payload = request.json_body
    except ValueError:
        raise HTTPBadRequest(json={'errors': {'body': ['Invalid JSON payload']}})

    schema = CategoryCreateSchema()
    try:
        category_data = schema.load(payload)
    except ValidationError as err:
        raise HTTPBadRequest(json={'errors': err.messages})

    # Check if category name already exists
    if CategoryService.get_category_by_name(request.dbsession, category_data['name']):
        raise HTTPBadRequest(
            json={'errors': {'name': ['Category with this name already exists']}}
        )

    category = CategoryService.create_category(request.dbsession, category_data)
    request.response.status = 201
    return CategorySchema().dump(category)


@view_config(route_name='api_v1.category', request_method='GET', renderer='json')
def get_category(request):
    """Get category by ID."""
    category_id = int(request.matchdict['id'])
    category = CategoryService.get_category_by_id(request.dbsession, category_id)
    if not category or not category.is_active:
        raise HTTPNotFound()
    return CategorySchema().dump(category)


@view_config(route_name='api_v1.category', request_method='PUT', renderer='json')
def update_category(request):
    """Update existing category."""
    category_id = int(request.matchdict['id'])
    category = CategoryService.get_category_by_id(request.dbsession, category_id)
    if not category or not category.is_active:
        raise HTTPNotFound()

    try:
        payload = request.json_body
    except ValueError:
        raise HTTPBadRequest(json={'errors': {'body': ['Invalid JSON payload']}})

    schema = CategoryUpdateSchema()
    try:
        update_data = schema.load(payload)
    except ValidationError as err:
        raise HTTPBadRequest(json={'errors': err.messages})

    # Check duplicate name when the name is being changed
    new_name = update_data.get('name')
    if new_name and new_name != category.name:
        if CategoryService.get_category_by_name(request.dbsession, new_name):
            raise HTTPBadRequest(
                json={'errors': {'name': ['Category with this name already exists']}}
            )

    updated_category = CategoryService.update_category(
        request.dbsession, category, update_data
    )
    return CategorySchema().dump(updated_category)


@view_config(route_name='api_v1.category', request_method='DELETE')
def delete_category(request):
    """Soft delete a category."""
    category_id = int(request.matchdict['id'])
    category = CategoryService.get_category_by_id(request.dbsession, category_id)
    if not category or not category.is_active:
        raise HTTPNotFound()
    CategoryService.delete_category(request.dbsession, category)
    return HTTPNoContent()
