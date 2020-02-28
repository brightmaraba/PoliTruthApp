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

        politician = Politician(name=data['name'])
        politician_list.append(politician)
        return politician.data, HTTPStatus.CREATED


class PoliticianResource(Resource):
    def get(self, politician_id):
        politician = next((politician for politician in politician_list
                           if politician_id == politician_id and politician.is_publish == True), None)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND

        return politician.data, HTTPStatus.OK

    def put(self, politician_id):
        data = request.get_json()

        politician = next((politician for politician in politician_list
                           if politician_id == politician_id and politician.is_publish == True), None)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.NOT_FOUND

        politician.name = data['name']

        return politician.data, HTTPStatus.OK

    def delete(self, politician_id):
        politician = next((politician for politician in politician_list
                           if politician_id == politician_id and politician.is_publish == True), None)

        if politician is None:
            return {'message': 'politician not found'}

        politician.is_publish = False


class PoliticianPublishResource(Resource):
    def put(self, politician_id):
        politician = next((politician for politician in politician_list
                           if politician_id == politician_id and politician.is_publish == True), None)

        if politician is None:
            return {'message': 'politician not found'}, HTTPStatus.OK

        politician.is_publish = True

        return {}, HTTPStatus.NO_CONTENT
