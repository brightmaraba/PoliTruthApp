# Import packages, classes and functions
from flask import Flask
from flask_restful import Api

from resources.politician import PoliticianListResource, PoliticianResource,PoliticianPublishResource

app =  Flask(__name__)
api = Api(app)

#Define Resource Routing

api.add_resourcees(PoliticianListResource, '/politicians')
api.add_resourcees(PoliticianResource, '/politician/<int:politician_id>')
api.add_resourcees(PoliticianPublishResource, '/politicians/<int:politician_id>/publish')

if __name__ =='__main__':
    app.run(port=5000, debug=True)

