import os
from extensions import image_set, cache, limiter
from utils import save_image, clear_cache
from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus
from webargs import fields
from webargs.flaskparser import use_kwargs

from models.politician import Politician
from schemas.politician import PoliticianSchema, PoliticianPaginationSchema

politician_schema = PoliticianSchema()
politician_list_schema = PoliticianSchema(many=True)
politician_cover_schema = PoliticianSchema(only=('cover_image', ))
politician_pagination_schema = PoliticianPaginationSchema()


class PoliticianListResource(Resource):
    decorators = [limiter.limit('10 per minute', methods=['GET'], error_message='Too Many Requests, Retry After 1 minute')]
    @use_kwargs({'q': fields.Str(missing=''),
                    'page': fields.Int(missing=1),
                    'per_page': fields.Int(missing=20),
                    'sort': fields.Str(missing='created_at'),
                    'order': fields.Str(missing='desc')
                    })
    @cache.cached(timeout=60, query_string=True)
    def get(self, q, page, per_page, sort, order):
        print('Querying database...')

        if sort not in['created_at', 'county', 'constituency']:
            sort = 'created_at'

        if order not in ['asc', 'desc']:
            order = 'desc'

        paginated_politicians = Politician.get_all_published(q, page, per_page, sort, order)

        return politician_pagination_schema.dump(paginated_politicians).data, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()

        current_user = get_jwt_identity()

        data, errors = politician_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        politician = Politician(**data)
        politician.user_id = current_user
        politician.save()

        return politician_schema.dump(politician).data, HTTPStatus.CREATED

class PoliticianResource(Resource):

    @jwt_optional
    def get(self, politician_id):

        politician = Politician.get_by_id(politician_id=politician_id)

        if politician is None:
            return {'message': 'Politician not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if politician.is_publish == False and politician.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return politician_schema.dump(politician).data, HTTPStatus.OK

    @jwt_required
    def patch(self, politician_id):

        json_data = request.get_json()

        data, errors = politician_schema.load(data=json_data, partial=True)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        politician = Politician.get_by_id(politician_id=politician_id)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != politician.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        politician.name = data.get('name') or politician.name
        politician.position = data.get('position') or politician.position
        politician.description = data.get('description') or politician.description
        politician.age = data.get('age') or politician.age
        politician.gender = data.get('gender') or politician.gender
        politician.bio_data = data.get('bio_data') or politician.bio_data
        politician.c_vitae = data.get('c_vitae') or politician.c_vitae
        politician.county = data.get('county') or politician.county
        politician.constituency = data.get('constituency') or politician.constituency
        politician.ward = data.get('ward') or politician.ward

        politician.save()

        clear_cache('/politicians')

        return politician_schema.dump(politician).data, HTTPStatus.OK

    @jwt_required
    def delete(self, politician_id):

        politician = Politician.get_by_id(politician_id=politician_id)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != politician.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        politician.delete()

        clear_cache('/politicians')

        return {}, HTTPStatus.NO_CONTENT


class PoliticianPublishResource(Resource):

    @jwt_required
    def put(self, politician_id):

        politician = Politician.get_by_id(politician_id=politician_id)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != politician.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        politician.is_publish = True
        politician.save()

        clear_cache('/politicians')

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, politician_id):

        politician = Politician.get_by_id(politician_id=politician_id)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != politician.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        politician.is_publish = False
        politician.save()

        clear_cache('/politicians')

        return {}, HTTPStatus.NO_CONTENT

class PoliticianCoverUploadResource(Resource):

    @jwt_required
    def put(self, politician_id):

        file = request.files.get('cover')

        if not file:
            return {'message': 'Not a valid image'}, HTTPStatus.BAD_REQUEST

        if not image_set.file_allowed(file, file.filename):
            return {'message': 'File type not allowed'}, HTTPStatus.BAD_REQUEST

        politician = Politician.get_by_id(politician_id=politician_id)

        if politician is None:
            return {'message': 'Politician not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != politician.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        if politician.cover_image:
            cover_path = image_set.path(folder='politicians', filename=politician.cover_image)
            if os.path.exists(cover_path):
                os.remove(cover_path)

        filename = save_image(image=file, folder='politicians')

        politician.cover_image = filename
        politician.save()

        clear_cache('/politicians')

        return politician_cover_schema.dump(politician).data, HTTPStatus.OK