from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from injector import inject

from backend.schemas.users_schema.user_update_schema import user_update_schema
from marshmallow import ValidationError
from backend.service.user_service import UserService

user_namespace = Namespace('User', description='User operations')


@user_namespace.route('/<uuid:user_id>/')
class UserDetail(Resource):
    @inject
    def __init__(self, user_service: UserService, **kwargs):
        super().__init__(**kwargs)
        self._user_service = user_service

    def get(self, user_id):
        try:
            user = self._user_service.get_by_id(user_id)
            return user, 200
        except ValueError as e:
            return {'error': str(e)}, 404

    @jwt_required
    def put(self, user_id):
        data = request.form.to_dict()
        avatar_file = request.files.get('avatarFile')
        try:
            validated_data = user_update_schema.load(data)
            updated_user = self._user_service.update_user(user_id, validated_data, avatar_file)
            return updated_user, 200
        except ValidationError as ve:
            return {'errors': ve.messages}, 400
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required
    def delete(self, user_id):
        try:
            self._user_service.delete_user(user_id)
            return 204
        except ValueError as e:
            return {'error': str(e)}, 404