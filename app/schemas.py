from marshmallow import Schema, fields


class SiteLoaderJsonSchema(Schema):
    url = fields.Str(required=True)
