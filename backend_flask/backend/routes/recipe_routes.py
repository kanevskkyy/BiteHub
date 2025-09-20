from json import loads
from uuid import UUID

from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, Namespace
from injector import inject
from marshmallow import ValidationError as MarshmallowValidationError

from backend.decorators.jwt_required_custom import jwt_required_custom
from backend.decorators.valid_image import validate_image_file
from backend.schemas.recipes.recipe_filter_schema import recipe_filter_schema
from backend.schemas.recipes.recipe_create_schema import recipe_create_schema
from backend.service.recipe_service import RecipeService
from backend.exceptions import NotFound, PermissionDenied, ValidationError as APIValidationError

recipe_namespace = Namespace('Recipe', description='Recipe related operations')


@recipe_namespace.route('/')
class RecipeList(Resource):
    @inject
    def __init__(self, recipe_service: RecipeService, **kwargs):
        super().__init__(**kwargs)
        self._recipe_service = recipe_service

    def get(self):
        args = request.args.to_dict(flat=True)
        for key in ['category_ids', 'ingredient_ids']:
            if key in args:
                args[key] = args.get(key, [])

        try:
            filters = recipe_filter_schema.load(args)
        except MarshmallowValidationError as err:
            return {'errors': err.messages}, 400

        recipes = self._recipe_service.get_recipes(filters)
        return recipes, 200

    @jwt_required_custom()
    @validate_image_file('photoUrl', required=True)
    def post(self):
        form_data = request.form.to_dict(flat=True)
        try:
            if 'steps' in form_data:
                form_data['steps'] = loads(form_data['steps'])
            if 'categoryIds' in form_data:
                form_data['categoryIds'] = loads(form_data['categoryIds'])
            if 'ingredientsIds' in form_data:
                form_data['ingredientsIds'] = loads(form_data['ingredientsIds'])

            data = recipe_create_schema.load(form_data)
        except MarshmallowValidationError as err:
            return {'errors': err.messages}, 400

        image_file = request.files.get('photoUrl')
        if not image_file:
            return {'errors': {'image': ['Image file is required']}}, 400

        try:
            recipe = self._recipe_service.create(data, image_file)
        except APIValidationError as e:
            return {'error': str(e)}, e.status_code

        return recipe, 201


@recipe_namespace.route('/<uuid:recipe_id>/')
class RecipeDetail(Resource):
    @inject
    def __init__(self, recipe_service: RecipeService, **kwargs):
        super().__init__(**kwargs)
        self._recipe_service = recipe_service

    def get(self, recipe_id: UUID):
        try:
            recipe = self._recipe_service.get_recipe_by_id(recipe_id)
        except NotFound as e:
            return {'error': str(e)}, e.status_code
        return recipe, 200

    @jwt_required_custom()
    @validate_image_file('photoUrl')
    def put(self, recipe_id: UUID):
        form_data = request.form.to_dict(flat=True)
        try:
            if 'steps' in form_data:
                form_data['steps'] = loads(form_data['steps'])
            if 'categoryIds' in form_data:
                form_data['categoryIds'] = loads(form_data['categoryIds'])
            if 'ingredientsIds' in form_data:
                form_data['ingredientsIds'] = loads(form_data['ingredientsIds'])

            data = recipe_create_schema.load(form_data)
        except MarshmallowValidationError as err:
            return {'errors': err.messages}, 400

        image_file = request.files.get('photoUrl')

        try:
            recipe = self._recipe_service.update(recipe_id, data, image_file)
        except (NotFound, PermissionDenied, APIValidationError) as e:
            return {'error': str(e)}, e.status_code

        return recipe, 200

    @jwt_required_custom()
    def delete(self, recipe_id: UUID):
        try:
            self._recipe_service.delete(recipe_id)
        except (NotFound, PermissionDenied) as e:
            return {'error': str(e)}, e.status_code
        return '', 204