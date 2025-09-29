from uuid import UUID

from flask import request
from flask_restx import Resource, Namespace
from injector import inject

from backend.decorators.jwt_required_custom import jwt_required_custom
from backend.decorators.role_required import role_required
from backend.pagination.pagination_schema import pagination_schema
from backend.schemas import review_schema, review_update_schema
from backend.service.review_service import ReviewService

review_namespace = Namespace('Review', description='Review related options')


@review_namespace.route('/')
class ReviewListResource(Resource):
    @inject
    def __init__(self, service: ReviewService, **kwargs):
        super().__init__(**kwargs)
        self._service = service

    @jwt_required_custom()
    def post(self):
        data = review_schema.load(request.get_json())
        created = self._service.create_review(data)
        return created, 201


@review_namespace.route('/<uuid:id>/')
class ReviewResource(Resource):
    @inject
    def __init__(self, service: ReviewService, **kwargs):
        super().__init__(**kwargs)
        self._service = service

    @jwt_required_custom()
    def put(self, id: UUID):
        data = review_update_schema.load(request.get_json())
        updated_review = self._service.update_review(id, data)
        return updated_review, 200

    @jwt_required_custom()
    def delete(self, id: UUID):
        self._service.delete_review(id)
        return '', 204


@review_namespace.route('/recipe/<uuid:id>/')
class ReviewByRecipeResource(Resource):
    @inject
    def __init__(self, service: ReviewService, **kwargs):
        super().__init__(**kwargs)
        self._service = service

    def get(self, id: UUID):
        data = pagination_schema.load(request.args.to_dict())
        page = data.get('page', 1)
        per_page = data.get('per_page', 10)
        reviews = self._service.get_reviews_by_recipe(id, page, per_page)
        return reviews, 200


@review_namespace.route('/pending/')
class PendingReviewsResource(Resource):
    @inject
    def __init__(self, service: ReviewService, **kwargs):
        super().__init__(**kwargs)
        self._service = service

    @jwt_required_custom()
    @role_required(['Admin'])
    def get(self):
        data = pagination_schema.load(request.args.to_dict())
        page = data.get('page', 1)
        per_page = data.get('per_page', 10)
        reviews = self._service.get_pending_reviews(page, per_page)
        return reviews, 200


@review_namespace.route('/<uuid:id>/approve/')
class ApproveReviewResource(Resource):
    @inject
    def __init__(self, service: ReviewService, **kwargs):
        super().__init__(**kwargs)
        self._service = service

    @jwt_required_custom()
    @role_required(['Admin'])
    def patch(self, id: UUID):
        self._service.approve_review(id)
        return {'message': 'Review approved successfully'}, 200