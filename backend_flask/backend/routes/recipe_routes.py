from json import loads

from flask import request
from flask_jwt_extended import jwt_required
from marshmallow import ValidationError
from flask_restx import Resource, Namespace
from injector import inject

from backend.decorators.valid_image import validate_image_file
from backend.schemas.recipes.recipe_filter_schema import recipe_filter_schema
from backend.schemas.recipes.recipe_create_schema import recipe_create_schema
from backend.service.recipe_service import RecipeService

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
        except ValidationError as err:
            return {'errors': err.messages}, 400

        recipes = self._recipe_service.get_recipes(filters)
        return recipes, 200

    @jwt_required()
    @validate_image_file('photoUrl', required=True)
    def post(self):
        try:
            form_data = request.form.to_dict(flat=True)
            if 'steps' in form_data:
                form_data['steps'] = loads(form_data['steps'])
            if 'categoryIds' in form_data:
                form_data['categoryIds'] = loads(form_data['categoryIds'])
            if 'ingredientsIds' in form_data:
                form_data['ingredientsIds'] = loads(form_data['ingredientsIds'])

            data = recipe_create_schema.load(form_data)
        except ValidationError as err:
            return {'errors': err.messages}, 400

        image_file = request.files.get('photoUrl')
        if not image_file:
            return {'errors': {'image': ['Image file is required']}}, 400

        recipe = self._recipe_service.create(data, image_file)
        return recipe, 201



@recipe_namespace.route('/<uuid:recipe_id>/')
class RecipeDetail(Resource):
    @inject
    def __init__(self, recipe_service: RecipeService, **kwargs):
        super().__init__(**kwargs)
        self._recipe_service = recipe_service

    def get(self, recipe_id):
        try:
            recipe = self._recipe_service.get_recipe_by_id(recipe_id)
        except ValueError as err:
            return {'error': str(err)}, 404
        return recipe, 200

    @jwt_required()
    @validate_image_file('photoUrl')
    def put(self, recipe_id):
        try:
            form_data = request.form.to_dict(flat=True)
            if 'steps' in form_data:
                form_data['steps'] = loads(form_data['steps'])
            if 'categoryIds' in form_data:
                form_data['categoryIds'] = loads(form_data['categoryIds'])
            if 'ingredientsIds' in form_data:
                form_data['ingredientsIds'] = loads(form_data['ingredientsIds'])

            data = recipe_create_schema.load(form_data)
        except ValidationError as err:
            return {'errors': err.messages}, 400

        image_file = request.files.get('photoUrl')

        try:
            recipe = self._recipe_service.update(recipe_id, data, image_file)
        except ValueError as err:
            return {'error': str(err)}, 404

        return recipe, 200

    @jwt_required()
    def delete(self, recipe_id):
        try:
            self._recipe_service.delete(recipe_id)
            return 204
        except ValueError as err:
            return {'error': str(err)}, 404