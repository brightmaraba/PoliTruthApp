from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db, jwt, image_set, cache, limiter
from flask_uploads import configure_uploads, patch_request_class


from resources.user import UserListResource, UserResource, MeResource, UserPoliticianListResource, UserActivateResource, UserAvatarUploadResource
from resources.token import TokenResource, RefreshResource, RevokeResource, black_list
from resources.politician import PoliticianListResource, PoliticianResource, PoliticianPublishResource, PoliticianCoverUploadResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)
    configure_uploads(app, image_set)
    patch_request_class(app, 10 * 1024 * 1024)
    cache.init_app(app)
    limiter.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in black_list


#    app.before_request
#    def before_request():
#        print('\n==================== BEFORE REQUEST ====================\n')
#        print(cache.cache._cache.keys())
#        print('\n=======================================================\n')
#
#    @app.after_request
#    def after_request(response):
#       print('\n==================== AFTER REQUEST ====================\n')
#        print(cache.cache._cache.keys())
#        print('\n=======================================================\n')
#       return response

#@limiter.request_filter
#def ip_whitelist():
#    return request.remote_addr == '127.0.0.1'

def register_resources(app):
    api = Api(app)

    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(UserPoliticianListResource, '/users/<string:username>/politicians')
    api.add_resource(UserActivateResource, '/users/activate/<string:token>')
    api.add_resource(UserAvatarUploadResource, '/users/avatar')

    api.add_resource(MeResource, '/me')

    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')

    api.add_resource(PoliticianListResource, '/politicians')
    api.add_resource(PoliticianResource, '/politicians/<int:politician_id>')
    api.add_resource(PoliticianPublishResource, '/politicians/<int:politician_id>/publish')
    api.add_resource(PoliticianCoverUploadResource, '/politicians/<int:politician_id>/cover')


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
