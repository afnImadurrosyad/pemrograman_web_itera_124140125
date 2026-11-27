from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    """Schema for product data validation."""

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=100))
    description = fields.String(validate=validate.Length(max=500), allow_none=True)
    price = fields.Float(required=True, validate=validate.Range(min=0.01))
    sku = fields.String(required=True, validate=validate.Length(min=5, max=50))
    category_id = fields.Integer(required=True)
    category = fields.Nested('CategorySchema', dump_only=True, exclude=('products',))
    is_active = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class ProductCreateSchema(ProductSchema):
    """Schema for product creation (without read-only fields)."""

    pass


class ProductUpdateSchema(Schema):
    """Schema for product updates (only updatable fields, SKU cannot change)."""

    name = fields.String(validate=validate.Length(min=2, max=100))
    description = fields.String(validate=validate.Length(max=500), allow_none=True)
    price = fields.Float(validate=validate.Range(min=0.01))
    category_id = fields.Integer()
    is_active = fields.Boolean()
