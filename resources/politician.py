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
        politician = Politician(
            name=data['name'],
            gender=data['gender'],
            age=data['age'],
            party=data['party'],
            position=data['position'],
            county=data['county'],
            constituency=data['constituency'],
            ward=data['ward'],
            bio_data=data['bio_data'],
            c_vitae=data['c_vitae'],
            description=data['description'])
        politician_list.append(politician)
        return politician.data, HTTPStatus.CREATED

class PoliticianResource(Resource):
    def get(self, politician_id):
        politician =  next((politician for politician in politician_list if politician_id ==
                        politician_id and politician.is_publish == True), None)
        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND
        return politician.data, HTTPStatus.OK

    def put(self, politician_id):
        data = request.get_json()
        politician = next((politician for politician in politician_list if politician_id ==
                        politician_id), None)
        if politician is None:
            return {'message'}, HTTPStatus.NOT_FOUND

        politician.name = data['name']
        politician.gender = data['gender']
        politician.age = data['age']
        politician.party = data['party']
        politician.position = data['position']
        politician.county = data['county']
        politician.constituency = data['constituency']
        politician.ward = data['ward']
        politician.bio_data = data['bio_data']
        politician.c_vitae = data['c_vitae']
        politician.description = data['description']

        return  politician.data, HTTPStatus.OK

class PoliticianPublishResource(Resource):
    def put(self, politician_id):
        politician = next((politician for politician in politician_list if politician_id ==
                        politician_id), None)
        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND
        politician.is_publish = True
        return {}, HTTPStatus.NO_CONTENT

    def delete(self, politician_id):
        politician_id = next((politician for politician in politician_list if politician_id ==
                        politician_id), None)
        if politician_id is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND
        politician.is_publish = False
        return {}, HTTPStatus.NO_CONTENT


