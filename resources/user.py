import os
from flask import request, url_for, render_template
from flask_restful import Resource
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from http import HTTPStatus

from utils import generate_token, verify_token, save_image, clear_cache

from mailgun import MailGunApi
from extensions import image_set, limiter
from utils import generate_token, verify_token, save_image


from webargs import fields
from webargs.flaskparser import use_kwargs

from models.politician import Politician
from models.user import User

from schemas.politician import PoliticianSchema, PoliticianPaginationSchema
from schemas.user import UserSchema


user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))
politician_list_schema = PoliticianSchema(many=True)
politician_pagination_schema = PoliticianPaginationSchema()
user_avatar_schema = UserSchema(only=('avatar_url', ))

mailgun = MailGunApi(domain=os.environ.get('MAILGUN_DOMAIN'),
                     api_key=os.environ.get('MAILGUN_API_KEY'))


class UserListResource(Resource):
    def post(self):

        json_data = request.get_json()

        current_user = get_jwt_identity()

        data, errors = user_schema.load(data=json_data)

        if errors:
            return {'message': 'Validation errors', 'errors': errors}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()
        token = generate_token(user.email, salt='activate')
        subject = 'Please Confirm Your Registration.'
        link = url_for('useractivateresource', token=token, _external=True)
        mailgun.send_email(to=user.email,
                            subject=subject,
                            html=render_template('email/confirmation.html', link=link))

        return user_schema.dump(user).data, HTTPStatus.CREATED


class UserActivateResource(Resource):
    def get(self, token):

        email = verify_token(token, salt='activate')

        if email is False:
            return {'message': 'Invalid toke or token expired'}, HTTPStatus.BAD_REQUEST

        user = User.get_by_email(email=email)
        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        if user.is_active is True:
            return {'message': 'The user account has been already activated'}, HTTPStatus.BAD_REQUEST
        user.is_active = True
        user.save()
        return {}, HTTPStatus.NO_CONTENT
class UserResource(Resource):

    @jwt_optional
    def get(self, username):

        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id:
            data = user_schema.dump(user).data
        else:
            data = user_public_schema.dump(user).data

        return data, HTTPStatus.OK


class MeResource(Resource):

    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())

        return user_schema.dump(user).data, HTTPStatus.OK

class UserPoliticianListResource(Resource):
    decorators = [limiter.limit('3/minute;30/hour;300/day',
                    methods=['GET'], error_message='Too Many Requests')]
    @jwt_optional
    @use_kwargs({'page': fields.Int(missing=1),
                'per_page': fields.Int(missing=10),
                'visibility': fields.Str(missing='public')})

    def get(self, username, page, per_page, visibility):

        user = User.get_by_username(username=username)

        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'

        paginated_politicians = Politician.get_all_by_user(user_id=user.id, page=page,
                                                           per_page=per_page, visibility=visibility)

        return politician_pagination_schema.dump(paginated_politicians).data, HTTPStatus.OK

class UserAvatarUploadResource(Resource):

    @jwt_required
    def put(self):

        file = request.files.get('avatar')

        if not file:
            return {'message': 'Not a valid image'}, HTTPStatus.BAD_REQUEST

        if not image_set.file_allowed(file, file.filename):
            return {'message': 'File type not allowed'}, HTTPStatus.BAD_REQUEST

        user = User.get_by_id(id=get_jwt_identity())

        if user.avatar_image:
            avatar_path = image_set.path(folder='avatars', filename=user.avatar_image)
            if os.path.exists(avatar_path):
                os.remove(avatar_path)

        filename = save_image(image=file, folder='avatars')

        user.avatar_image = filename
        user.save()

        clear_cache('/politicians')

        return user_avatar_schema.dump(user).data, HTTPStatus.OK