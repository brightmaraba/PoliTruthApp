from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db
from resources.user import UserListResource

from resources.politician import PoliticianListResource, PoliticianResource, PoliticianPublishResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)
    set_context(app)

    return(app)

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)

def register_resources(app):
    api = Api(app)

    api.add_resource(PoliticianListResource, '/politicians')
    api.add_resource(PoliticianResource, '/politicians/<int:politician_id>')
    api.add_resource(PoliticianPublishResource, '/politicians/<int:politician_id>/publish')
    api.add_resource(UserListResource,'/users')

def set_context(app):
    app.app_context().push()

if __name__ == '__main__':
    app.run(port=5000, debug=True)
