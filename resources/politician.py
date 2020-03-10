from flask import request
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from http import HTTPStatus

from models.politician import Politician
from schemas.politician import PoliticianSchema

politician_schema = PoliticianSchema()
politician_list_schema = PoliticianSchema(many=True)


class PoliticianListResource(Resource):

    def get(self):

        politicians = Politician.get_all_published()

        return politician_list_schema.dump(politicians).data, HTTPStatus.OK

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

        data, errors = politician_schema.load(data=json_data, partial=('name',))

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        politician = Politician.get_by_id(politician_id=politician_id)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != politician.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        politician.name = json_data['name']
        politician.position = json_data['position']
        politician.description = json_data['description']
        politician.age = json_data['age']
        politician.gender = json_data['gender']
        politician.bio_data = json_data['bio_data']
        politician.c_vitae = json_data['c_vitae']
        politician.county = json_data['county']
        politician.constituency = json_data['constituency']
        politician.ward = json_data['ward']

        politician.save()

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

        return {}, HTTPStatus.NO_CONTENT
