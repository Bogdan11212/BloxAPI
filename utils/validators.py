from marshmallow import Schema, fields, ValidationError, validate

# Generic validators
class PaginationSchema(Schema):
    """Pagination parameters schema"""
    limit = fields.Integer(validate=validate.Range(min=1, max=100), default=10)
    cursor = fields.String(default=None)

class SearchSchema(Schema):
    """Search parameters schema"""
    keyword = fields.String(required=True, validate=validate.Length(min=1))
    limit = fields.Integer(validate=validate.Range(min=1, max=100), default=10)

# User-related validators
class UserIdListSchema(Schema):
    """Schema for validating a list of user IDs"""
    userIds = fields.List(
        fields.Integer(validate=validate.Range(min=1)), 
        required=True,
        validate=validate.Length(min=1, max=100)
    )

class UsernameListSchema(Schema):
    """Schema for validating a list of usernames"""
    usernames = fields.List(
        fields.String(validate=validate.Length(min=3, max=20)), 
        required=True,
        validate=validate.Length(min=1, max=100)
    )

# Game-related validators
class GameSearchSchema(Schema):
    """Schema for game search parameters"""
    keyword = fields.String(default=None)
    sort_order = fields.String(
        default="Asc", 
        validate=validate.OneOf(["Asc", "Desc"])
    )
    genre = fields.String(default=None)
    limit = fields.Integer(validate=validate.Range(min=1, max=100), default=10)
    cursor = fields.String(default=None)

# Group-related validators
class GroupMembersSchema(Schema):
    """Schema for group members query parameters"""
    limit = fields.Integer(validate=validate.Range(min=1, max=100), default=10)
    sort_order = fields.String(
        default="Asc", 
        validate=validate.OneOf(["Asc", "Desc"])
    )
    role_id = fields.Integer(default=None)
    cursor = fields.String(default=None)

# Catalog-related validators
class CatalogSearchSchema(Schema):
    """Schema for catalog search parameters"""
    keyword = fields.String(required=True, validate=validate.Length(min=1))
    category = fields.String(default=None)
    subcategory = fields.String(default=None)
    sort_type = fields.String(
        default="Relevance", 
        validate=validate.OneOf([
            "Relevance", "Favorited", "Sales", "Updated", "PriceAsc", "PriceDesc"
        ])
    )
    min_price = fields.Integer(validate=validate.Range(min=0), default=None)
    max_price = fields.Integer(validate=validate.Range(min=0), default=None)
    limit = fields.Integer(validate=validate.Range(min=1, max=100), default=10)
    cursor = fields.String(default=None)

# Asset-related validators
class AssetInfoSchema(Schema):
    """Schema for asset information query parameters"""
    include_purchase_count = fields.Boolean(default=False)
    include_creator = fields.Boolean(default=True)
