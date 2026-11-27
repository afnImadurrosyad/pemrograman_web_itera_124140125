from marshmallow import Schema, fields, validate


class CategorySchema(Schema):
    """Schema for category data validation."""

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    description = fields.String(validate=validate.Length(max=500), allow_none=True)
    is_active = fields.Boolean()
    products = fields.Nested('ProductSchema', many=True, dump_only=True,
                             exclude=('category',), attribute='active_products')
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class CategoryCreateSchema(CategorySchema):
    """Schema for category creation (without read-only fields)."""

    pass


class CategoryUpdateSchema(Schema):
    """Schema for category updates (only updatable fields)."""

    name = fields.String(validate=validate.Length(min=2, max=100))
    description = fields.String(validate=validate.Length(max=500), allow_none=True)
    is_active = fields.Boolean()
