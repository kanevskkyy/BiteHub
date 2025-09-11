from flask_restx import Namespace, Resource
from flask import request
from injector import inject
from marshmallow import ValidationError

from backend.pagination.pagination_schema import pagination_schema
from backend.schemas.review_schemas.review_schema import review_schema
from backend.schemas.review_schemas.review_update_schema import review_update_schema
from backend.service.review_service import ReviewService

review_namespace = Namespace('Review', description='Review related options')

@review_namespace.route('/<uuid:id>/')
class Review(Resource):
    @inject
    def __init__(self, review_service: ReviewService, **kwargs):
        super().__init__(**kwargs)
        self._review_service = review_service

    def put(self, id):
        try:
            data = review_update_schema.load(request.get_json())
            updated_review = self._review_service.update_review(id, data)

            return updated_review, 200
        except ValidationError as ve:
            return {'errors': ve.messages}, 400
        except ValueError as e:
            return {'error': str(e)}, 400

    def delete(self, id):
        try:
            self._review_service.delete_review(id)
            return 204
        except ValueError as e:
            return {'error': str(e)}, 404


@review_namespace.route('/recipe/<uuid:id>/')
class ReviewByRecipeResource(Resource):
    @inject
    def __init__(self, service: ReviewService, **kwargs):
        super().__init__(**kwargs)
        self._service = service

    def get(self, id):
        try:
            data = pagination_schema.load(request.args.to_dict())
            page = data['page']
            per_page = data['per_page']
            reviews = self._service.get_reviews_by_recipe(id, page, per_page)
            return reviews, 200
        except ValueError as e:
            return {'error': str(e)}, 400



@review_namespace.route('/')
class ReviewListResource(Resource):
    @inject
    def __init__(self, service: ReviewService, **kwargs):
        super().__init__(**kwargs)
        self._service = service

    def post(self):
        try:
            data = review_schema.load(request.get_json())
            created = self._service.create_review(data)
            return created, 201

        except ValidationError as err:
            return {'errors': err.messages}, 400

        except ValueError as err:
            return {'message': str(err)}, 400