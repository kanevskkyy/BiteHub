from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_restx import Namespace, Resource
from injector import inject

from backend.decorators.jwt_required_custom import jwt_required_custom
from backend.decorators.valid_image import validate_image_file
from backend.extensions import limiter
from backend.schemas import user_update_schema
from backend.service.user_service import UserService

user_namespace = Namespace('User', description='User operations')


@user_namespace.route('/<uuid:user_id>/')
class UserDetail(Resource):
    @inject
    def __init__(self, user_service: UserService, **kwargs):
        super().__init__(**kwargs)
        self._user_service = user_service

    def get(self, user_id):
        user = self._user_service.get_by_id(user_id)
        return user, 200

    @jwt_required_custom()
    @validate_image_file('avatarFile')
    @limiter.limit('5 per minute')
    def put(self, user_id):
        data = request.form.to_dict()
        avatar_file = request.files.get('avatarFile')
        validated_data = user_update_schema.load(data)
        updated_user = self._user_service.update_user(user_id, validated_data, avatar_file)
        return updated_user, 200

    @jwt_required_custom()
    def delete(self, user_id):
        self._user_service.delete_user(user_id)
        return 204

@user_namespace.route('/me/')
class UserMe(Resource):
    @inject
    def __init__(self, user_service: UserService, **kwargs):
        super().__init__(**kwargs)
        self._user_service = user_service

    @jwt_required_custom()
    def get(self):
        user_id = get_jwt_identity()
        user = self._user_service.get_by_id(user_id)
        return user, 200