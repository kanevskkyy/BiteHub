from flask import request
from flask_restx import Namespace, Resource
from injector import inject
from marshmallow import ValidationError as MarshmallowValidationError

from backend.decorators.jwt_required_custom import jwt_required_custom
from backend.decorators.role_required import role_required
from backend.decorators.valid_image import validate_image_file
from backend.schemas import category_schema
from backend.service import CategoryService
from backend.exceptions import NotFound, AlreadyExists, ValidationError as APIValidationError

category_namespace = Namespace('Category', description='Category related operations')


@category_namespace.route('/')
class CategoryList(Resource):
    @inject
    def __init__(self, category_service: CategoryService, **kwargs):
        super().__init__(**kwargs)
        self._category_service = category_service

    def get(self):
        categories = self._category_service.get_all()
        return categories, 200

    @jwt_required_custom()
    @role_required(['Admin'])
    @validate_image_file('iconFile', required=True)
    def post(self):
        data = request.form.to_dict()
        icon_file = request.files.get('iconFile')
        try:
            validated_data = category_schema.load(data)
            new_category = self._category_service.create(validated_data, icon_file)
            return new_category, 201
        except (AlreadyExists, APIValidationError) as e:
            return {'error': str(e)}, e.status_code
        except MarshmallowValidationError as ve:
            return {'errors': ve.messages}, 400


@category_namespace.route('/<uuid:id>/')
class CategoryItem(Resource):
    @inject
    def __init__(self, category_service: CategoryService, **kwargs):
        super().__init__(**kwargs)
        self._category_service = category_service

    def get(self, id):
        try:
            category = self._category_service.get_by_id(id)
            return category, 200
        except NotFound as e:
            return {'error': str(e)}, e.status_code

    @jwt_required_custom()
    @role_required(['Admin'])
    @validate_image_file('iconFile')
    def put(self, id):
        data = request.form.to_dict()
        icon_file = request.files.get('iconFile')
        try:
            validated_data = category_schema.load(data)
            updated_category = self._category_service.update(id, validated_data, icon_file)
            return updated_category, 200
        except (NotFound, AlreadyExists, APIValidationError) as e:
            return {'error': str(e)}, e.status_code
        except MarshmallowValidationError as ve:
            return {'errors': ve.messages}, 400

    @jwt_required_custom()
    @role_required(['Admin'])
    def delete(self, id):
        try:
            self._category_service.delete(id)
            return '', 204
        except NotFound as e:
            return {'error': str(e)}, e.status_code