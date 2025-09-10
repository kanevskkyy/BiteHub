from flask import request
from flask_restx import Namespace, Resource
from injector import inject
from marshmallow import ValidationError

from backend.schemas.users_schema.user_create_schema import user_create_schema
from backend.service.auth_service import AuthService

auth_namespace = Namespace('Auth', description='Authorization actions')

@auth_namespace.route('/register/')
class RegisterResource(Resource):
    @inject
    def __init__(self, auth_service: AuthService, **kwargs):
        super().__init__(**kwargs)
        self._auth_service = auth_service

    def post(self):
        try:
            data = user_create_schema.load(request.form)
            avatar_file = request.files.get('avatarFile')

            result = self._auth_service.register_user(data)
            return result, 200
        except ValidationError as e:
            return e.messages, 400
        except ValueError as e:
            return {
                'error': str(e),
            }, 400