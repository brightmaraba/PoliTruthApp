from marshmallow import Schema, fields, post_dump, validate, validates, ValidationError
from schemas.user import UserSchema

class PoliticianSchema(Schema):
    class Meta:
        ordered = True

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[validate.Length(max=100)])
    position = fields.String(required=True, validate=[validate.Length(max=100)])
    description = fields.String(required=True, validate=[validate.Length(max=300)])
    age = fields.Integer(required=True)
    gender = fields.String(required=True, validate=[validate.Length(max=10)])
    bio_data = fields.String(required=True, validate=[validate.Length(max=5000)])
    c_vitae = fields.String(required=True, validate=[validate.Length(max=10000)])
    county = fields.String(required=True, validate=[validate.Length(max=100)])
    constituency =  fields.String(required=True, validate=[validate.Length(max=100)])
    ward = fields.String(required=True, validate=[validate.Length(max=100)])
    is_publish = fields.Boolean(dump_only=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    author = fields.Nested(UserSchema, attribute='user', dump_only=True,
                            only=['id', 'username'])

    @validates('age')
    def validate_age(self, value):
        if value < 18:
            raise ValidationError('Politician age must be older than 18.')
        if value > 90:
            raise ValidationError('Politician should be younger than 90.')