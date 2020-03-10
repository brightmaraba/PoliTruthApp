from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError

from schemas.user import UserSchema


def validate_age(n):
    if n < 18:
        raise ValidationError('Politician cannot be under 18.')
    if n > 80:
        raise ValidationError('Politician cannot be older than 90.')


class PoliticianSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    position = fields.String(required=True, validate=[validate.Length(max=100)])
    description = fields.String(validate=[validate.Length(max=200)])
    age = fields.Integer(validate=validate_age)
    gender = fields.String(required=True, validate=[validate.Length(max=10)])
    bio_data = fields.String(required=True, validate=[validate.Length(max=5000)])
    c_vitae = fields.String(required=True, validate=[validate.Length(max=10000)])
    county = fields.String(required=True, validate=[validate.Length(max=100)])
    constituency =  fields.String(required=True, validate=[validate.Length(max=100)])
    ward = fields.String(required=True, validate=[validate.Length(max=100)])
    is_publish = fields.Boolean(dump_only=True)

    author = fields.Nested(UserSchema, attribute='user', dump_only=True, only=['id', 'username'])

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many, **kwargs):
        if many:
            return {'data': data}
        return data