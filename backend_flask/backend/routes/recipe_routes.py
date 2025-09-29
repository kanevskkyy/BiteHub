from json import loads
from uuid import UUID

from flask import request
from flask_restx import Resource, Namespace
from injector import inject

from backend.decorators.jwt_required_custom import jwt_required_custom
from backend.decorators.valid_image import validate_image_file
from backend.schemas import recipe_filter_schema, recipe_create_schema
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

        for key in ['categoryIds', 'ingredientIds']:
            if key in request.args:
                args[key] = request.args.getlist(key)

            filters = recipe_filter_schema.load(args)

        recipes = self._recipe_service.get_recipes(filters)
        return recipes, 200

    @jwt_required_custom()
    @validate_image_file('photoUrl', required=True)
    def post(self):
        form_data = request.form.to_dict(flat=True)

        if 'steps' in form_data:
            form_data['steps'] = loads(form_data['steps'])
        if 'categoryIds' in form_data:
            form_data['categoryIds'] = loads(form_data['categoryIds'])
        if 'ingredientsIds' in form_data:
            form_data['ingredientsIds'] = loads(form_data['ingredientsIds'])

        data = recipe_create_schema.load(form_data)

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

    @jwt_required_custom(optional=True)
    def get(self, recipe_id: UUID):

        recipe = self._recipe_service.get_recipe_by_id(recipe_id)

        return recipe, 200,

    @jwt_required_custom()
    @validate_image_file('photoUrl')
    def put(self, recipe_id: UUID):
        form_data = request.form.to_dict(flat=True)

        if 'steps' in form_data:
            form_data['steps'] = loads(form_data['steps'])
        if 'categoryIds' in form_data:
            form_data['categoryIds'] = loads(form_data['categoryIds'])
        if 'ingredientsIds' in form_data:
            form_data['ingredientsIds'] = loads(form_data['ingredientsIds'])

        data = recipe_create_schema.load(form_data)
        image_file = request.files.get('photoUrl')

        recipe = self._recipe_service.update(recipe_id, data, image_file)
        return recipe, 200


    @jwt_required_custom()
    def delete(self, recipe_id: UUID):
        self._recipe_service.delete(recipe_id)
        return 204