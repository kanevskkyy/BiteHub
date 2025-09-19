from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from flask import request
from injector import inject
from marshmallow import ValidationError

from backend.decorators.role_required import role_required
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

    @jwt_required()
    def put(self, id):
        try:
            data = review_update_schema.load(request.get_json())
            updated_review = self._review_service.update_review(id, data)

            return updated_review, 200
        except ValidationError as ve:
            return {'errors': ve.messages}, 400
        except ValueError as e:
            return {'error': str(e)}, 400

    @jwt_required()
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

    @jwt_required()
    def post(self):
        try:
            data = review_schema.load(request.get_json())
            created = self._service.create_review(data)
            return created, 201

        except ValidationError as err:
            return {'errors': err.messages}, 400

        except ValueError as err:
            return {'message': str(err)}, 400


@review_namespace.route('/pending/')
class PendingReviewsResource(Resource):
    @inject
    def __init__(self, service: ReviewService, **kwargs):
        super().__init__(**kwargs)
        self._service = service

    @jwt_required()
    @role_required(['Admin'])
    def get(self):
        try:
            data = pagination_schema.load(request.args.to_dict())
            page = data.get('page', 1)
            per_page = data.get('per_page', 10)

            reviews = self._service.get_pending_reviews(page, per_page)
            return reviews, 200

        except ValueError as err:
            return {'error': str(err)}, 400
        except ValidationError as ve:
            return {'errors': ve.messages}, 400


@review_namespace.route('/<uuid:id>/approve/')
class ApproveReviewResource(Resource):
    @inject
    def __init__(self, service: ReviewService, **kwargs):
        super().__init__(**kwargs)
        self._service = service

    @jwt_required()
    @role_required(['Admin'])
    def patch(self, id):
        try:
            self._service.approve_review(id)
            return {
                'message': 'Review approved successfully',
            }, 200
        except ValueError as err:
            return {'error': str(err)}, 400