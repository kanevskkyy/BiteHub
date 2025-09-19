from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from injector import inject
from marshmallow import ValidationError as MarshmallowValidationError

from backend.decorators.valid_image import validate_image_file
from backend.schemas.users_schema.user_update_schema import user_update_schema
from backend.service.user_service import UserService
from backend.exceptions import NotFound, PermissionDenied, AlreadyExists, ValidationError as APIValidationError

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
        except NotFound as e:
            return {'error': str(e)}, e.status_code

    @jwt_required()
    @validate_image_file('avatarFile')
    def put(self, user_id):
        try:
            data = request.form.to_dict()
            avatar_file = request.files.get('avatarFile')
            validated_data = user_update_schema.load(data)
            updated_user = self._user_service.update_user(user_id, validated_data, avatar_file)
            return updated_user, 200
        except MarshmallowValidationError as err:
            return {'errors': err.messages}, 400
        except (NotFound, PermissionDenied, AlreadyExists, APIValidationError) as e:
            return {'error': str(e)}, e.status_code

    @jwt_required()
    def delete(self, user_id):
        try:
            self._user_service.delete_user(user_id)
            return '', 204
        except (NotFound, PermissionDenied) as e:
            return {'error': str(e)}, e.status_code