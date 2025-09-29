from flask import request
from flask_restx import Namespace, Resource
from injector import inject
from backend.decorators.jwt_required_custom import jwt_required_custom
from backend.decorators.valid_image import validate_image_file
from backend.schemas import user_create_schema, login_schema, change_password_schema
from backend.service.auth_service import AuthService

auth_namespace = Namespace('Auth', description='Authorization actions')


@auth_namespace.route('/register/')
class RegisterResource(Resource):
    @inject
    def __init__(self, auth_service: AuthService, **kwargs):
        super().__init__(**kwargs)
        self._auth_service = auth_service

    @validate_image_file('avatarFile')
    def post(self):
        data = user_create_schema.load(request.form)
        avatar_file = request.files.get('avatarFile')
        result = self._auth_service.register_user(data, avatar_file)
        return result, 200


@auth_namespace.route('/login/')
class LoginResource(Resource):
    @inject
    def __init__(self, auth_service: AuthService, **kwargs):
        super().__init__(**kwargs)
        self._auth_service = auth_service

    def post(self):
        data = login_schema.load(request.get_json())
        result = self._auth_service.login_user(data)
        return result, 200


@auth_namespace.route('/refresh-token/')
class RefreshTokenResource(Resource):
    @inject
    def __init__(self, auth_service: AuthService, **kwargs):
        super().__init__(**kwargs)
        self._auth_service = auth_service

    @jwt_required_custom(refresh=True)
    def post(self):
        access_token = self._auth_service.refresh_access_token()
        return {'accessToken': access_token}, 200


@auth_namespace.route('/change-password/')
class ChangePasswordResource(Resource):
    @inject
    def __init__(self, auth_service: AuthService, **kwargs):
        super().__init__(**kwargs)
        self._auth_service = auth_service

    @jwt_required_custom()
    def post(self):
        data = change_password_schema.load(request.get_json())
        self._auth_service.change_password(data)
        return {'message': 'Password changed successfully'}, 200


@auth_namespace.route('/check-username/<string:username>/')
class CheckUsernameResource(Resource):
    @inject
    def __init__(self, auth_service: AuthService, **kwargs):
        super().__init__(**kwargs)
        self._auth_service = auth_service

    def get(self, username):
        result = self._auth_service.check_username_exist(username)
        return result, 200