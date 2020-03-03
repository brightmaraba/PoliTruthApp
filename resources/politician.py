from flask import request
from flask_restful import Resource
from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from models.politician import Politician


class PoliticianListResource(Resource):

    def get(self):
        politicians = Politician.get_all_published()
#Test if it works
        if politicians is None:
            return {'message': 'No politicians found'}, HTTPStatus.NOT_FOUND

        data = []

        for politician in politicians:
            data.append(politician.data())

        return {'data': data}, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()
        current_user = get_jwt_identity()
        politician = Politician(name = json_data['name'],
                                position = json_data['position'],
                                description = json_data['description'],
                                age = json_data['age'],
                                gender = json_data['gender'],
                                bio_data = json_data['bio_data'],
                                c_vitae = json_data['c_vitae'],
                                county = json_data['county'],
                                constituency = json_data['constituency'],
                                ward = json_data['ward'],
                                user_id = current_user)

        politician.save()

        return politician.data(), HTTPStatus.CREATED


class PoliticianResource(Resource):
    @jwt_optional
    def get(self, politician_id):
        politician = Politician.get_by_id(politician_id=politician_id)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if politician.is_publish == False and politician.user_id !=current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return politician.data(), HTTPStatus.OK

    @jwt_required
    def put(self, politician_id):
        json_data = request.get_json()

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

        return politician.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, politician_id):

        politician = Politician.get_by_id(politician_id=politician_id)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()
        if current_user != politician.user_id:
            return {'message': "Access is not allowed"}, HTTPStatus.FORBIDDEN

        politician.delete()

        return {}, HTTPStatus.NO_CONTENT


class PoliticianPublishResource(Resource):

    def put(self, politician_id):
        politician = next((politician for politician in politician_list if politician.id == politician_id), None)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND

        politician.is_publish = True

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, politician_id):
        politician = next((politician for politician in politician_list if politician.id == politician_id), None)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND

        politician.is_publish = False

        return {}, HTTPStatus.NO_CONTENT
