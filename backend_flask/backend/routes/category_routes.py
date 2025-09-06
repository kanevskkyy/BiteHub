from flask import request
from flask_restx import Namespace, Resource
from injector import inject
from marshmallow import ValidationError
from backend.service import CategoryService


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

    def post(self):
        data = request.form.to_dict()
        icon_file = request.files.get('iconFile')
        try:
            new_category = self._category_service.create(data, icon_file)
            return new_category, 201
        except ValidationError as e:
            return {'error': e.messages}, 400


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
        except ValueError as e:
            return {'error': str(e)}, 404

    def put(self, id):
        data = request.form.to_dict()
        icon_file = request.files.get('iconFile')
        try:
            updated_category = self._category_service.update(id, data, icon_file)
            return updated_category, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except ValidationError as ve:
            return {'errors': ve.messages}, 400

    def delete(self, id):
        try:
            self._category_service.delete(id)
            return {'message': f'Category {id} deleted successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 404