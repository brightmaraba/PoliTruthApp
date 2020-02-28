from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.politician import Politician, politician_list


class PoliticianListResource(Resource):

    def get(self):

        data = []

        for politician in politician_list:
            if politician.is_publish is True:
                data.append(politician.data)

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        politician = Politician(name=data['name'],
                                position=data['position'],
                                description=data['description'],
                                age=data['age'],
                                gender=data['gender'],
                                bio_data=data['bio_data'],
                                c_vitae=data['c_vitae'],
                                county=data['county'],
                                constituency=data['constituency'],
                                ward=data['ward']
        )

        politician_list.append(politician)

        return politician.data, HTTPStatus.CREATED


class PoliticianResource(Resource):

    def get(self, politician_id):
        politician = next((politician for politician in politician_list if politician.id == politician_id and politician.is_publish == True), None)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND

        return politician.data, HTTPStatus.OK

    def put(self, politician_id):
        data = request.get_json()

        politician = next((politician for politician in politician_list if politician.id == politician_id), None)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND

        politician.name = data['name']
        politician.position = data['position']
        politician.description = data['description']
        politician.age = data['age']
        politician.gender = data['gender']
        politician.bio_data = data['bio_data']
        politician.c_vitae = data['c_vitae']
        politician.county = data['county']
        politician.constituency = data['constituency']
        politician.ward = data['ward']

        return politician.data, HTTPStatus.OK

    def delete(self, politician_id):

        politician = next((politician for politician in politician_list if politician.id == politician_id), None)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND

        politician_list.remove(politician)

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
