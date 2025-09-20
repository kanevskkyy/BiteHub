from flask import request
from flask_restx import Namespace, Resource
from injector import inject
from marshmallow import ValidationError as MarshmallowValidationError

from backend.decorators.jwt_required_custom import jwt_required_custom
from backend.decorators.valid_image import validate_image_file
from backend.schemas.auth.change_password import change_password_schema
from backend.schemas.auth.login_schema import login_schema
from backend.schemas.auth.user_create_schema import user_create_schema
from backend.service.auth_service import AuthService
from backend.exceptions import AlreadyExists, NotFound, ValidationError

auth_namespace = Namespace('Auth', description='Authorization actions')


@auth_namespace.route('/register/')
class RegisterResource(Resource):
    @inject
    def __init__(self, auth_service: AuthService, **kwargs):
        super().__init__(**kwargs)
        self._auth_service = auth_service

    @validate_image_file('avatarFile')
    def post(self):
        try:
            data = user_create_schema.load(request.form)
            avatar_file = request.files.get('avatarFile')
            result = self._auth_service.register_user(data, avatar_file)
            return result, 200

        except MarshmallowValidationError as e:
            return {'errors': e.messages}, 400
        except (AlreadyExists, ValidationError, NotFound) as e:
            return {'error': str(e)}, e.status_code


@auth_namespace.route('/login/')
class LoginResource(Resource):
    @inject
    def __init__(self, auth_service: AuthService, **kwargs):
        super().__init__(**kwargs)
        self._auth_service = auth_service

    def post(self):
        try:
            data = login_schema.load(request.get_json())
            result = self._auth_service.login_user(data)
            return result, 200

        except MarshmallowValidationError as e:
            return {'errors': e.messages}, 400
        except ValidationError as e:
            return {'error': str(e)}, e.status_code


@auth_namespace.route('/refresh-token/')
class RefreshTokenResource(Resource):
    @inject
    def __init__(self, auth_service: AuthService, **kwargs):
        super().__init__(**kwargs)
        self._auth_service = auth_service

    @jwt_required_custom(refresh=True)
    def post(self):
        try:
            access_token = self._auth_service.refresh_access_token()
            return {'accessToken': access_token}, 200

        except NotFound as e:
            return {'error': str(e)}, e.status_code


@auth_namespace.route('/change-password/')
class ChangePasswordResource(Resource):
    @inject
    def __init__(self, auth_service: AuthService, **kwargs):
        super().__init__(**kwargs)
        self._auth_service = auth_service

    @jwt_required_custom()
    def post(self):
        try:
            data = change_password_schema.load(request.get_json())
            self._auth_service.change_password(data)
            return {'message': 'Password changed successfully'}, 200

        except MarshmallowValidationError as e:
            return {'errors': e.messages}, 400
        except ValidationError as e:
            return {'error': str(e)}, e.status_code
        except NotFound as e:
            return {'error': str(e)}, e.status_code