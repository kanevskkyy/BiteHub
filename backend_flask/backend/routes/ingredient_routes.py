from uuid import UUID
from flask import request
from flask_restx import Namespace, Resource
from injector import inject

from backend.decorators.jwt_required_custom import jwt_required_custom
from backend.decorators.role_required import role_required
from backend.decorators.valid_image import validate_image_file
from backend.schemas import ingredient_schema
from backend.service.ingredient_service import IngredientsService

ingredient_namespace = Namespace('Ingredient', description='Ingredient related operations')


@ingredient_namespace.route('/')
class IngredientList(Resource):
    @inject
    def __init__(self, ingredient_service: IngredientsService, **kwargs):
        super().__init__(**kwargs)
        self._ingredient_service = ingredient_service

    def get(self):
        ingredients = self._ingredient_service.get_all()
        return ingredients, 200

    @jwt_required_custom()
    @role_required(['Admin'])
    @validate_image_file('iconFile', required=True)
    def post(self):
        data = request.form.to_dict()
        icon_file = request.files.get('iconFile')

        validated_data = ingredient_schema.load(data)
        new_ingredient = self._ingredient_service.create(validated_data, icon_file)
        return new_ingredient, 201


@ingredient_namespace.route('/<uuid:id>/')
class IngredientItem(Resource):
    @inject
    def __init__(self, ingredient_service: IngredientsService, **kwargs):
        super().__init__(**kwargs)
        self._ingredient_service = ingredient_service

    def get(self, id: UUID):
        ingredient = self._ingredient_service.get_by_id(id)
        return ingredient, 200

    @jwt_required_custom()
    @role_required(['Admin'])
    @validate_image_file('iconFile')
    def put(self, id: UUID):
        data = request.form.to_dict()
        icon_file = request.files.get('iconFile')

        validated_data = ingredient_schema.load(data)
        updated_ingredient = self._ingredient_service.update(id, validated_data, icon_file)
        return updated_ingredient, 200


    @jwt_required_custom()
    @role_required(['Admin'])
    def delete(self, id: UUID):
        self._ingredient_service.delete(id)
        return 204