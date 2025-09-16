from uuid import UUID
from flask import request
from flask_restx import Namespace, Resource
from injector import inject
from marshmallow import ValidationError

from backend.decorators.role_required import role_required
from backend.schemas.ingredient_schema import ingredient_schema
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

    @role_required(['Admin'])
    def post(self):
        data = request.form.to_dict()
        icon_file = request.files.get('iconFile')
        try:
            validated_data = ingredient_schema.load(data)
            new_ingredient = self._ingredient_service.create(validated_data, icon_file)
            return new_ingredient, 201
        except ValidationError as ve:
            return {'errors': ve.messages}, 400
        except ValueError as e:
            return {'error': str(e)}, 400


@ingredient_namespace.route('/<uuid:id>/')
class IngredientItem(Resource):
    @inject
    def __init__(self, ingredient_service: IngredientsService, **kwargs):
        super().__init__(**kwargs)
        self._ingredient_service = ingredient_service

    def get(self, id: UUID):
        try:
            ingredient = self._ingredient_service.get_by_id(id)
            return ingredient, 200
        except ValueError as e:
            return {'error': str(e)}, 404

    @role_required(['Admin'])
    def put(self, id: UUID):
        data = request.form.to_dict()
        icon_file = request.files.get('icon File')
        try:
            validated_data = ingredient_schema.load(data)
            updated_ingredient = self._ingredient_service.update(id, validated_data, icon_file)
            return updated_ingredient, 200
        except ValidationError as ve:
            return {'errors': ve.messages}, 400
        except ValueError as e:
            return {'error': str(e)}, 400

    @role_required(['Admin'])
    def delete(self, id: UUID):
        try:
            self._ingredient_service.delete(id)
            return 204
        except ValueError as e:
            return {'error': str(e)}, 404
