from uuid import UUID
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Resource, Namespace
from injector import inject
from marshmallow import ValidationError as MarshmallowValidationError

from backend.decorators.role_required import role_required
from backend.pagination.pagination_schema import pagination_schema
from backend.schemas.review_schemas.review_schema import review_schema
from backend.schemas.review_schemas.review_update_schema import review_update_schema
from backend.service.review_service import ReviewService
from backend.exceptions import NotFound, AlreadyExists, PermissionDenied, ValidationError as APIValidationError

review_namespace = Namespace('Review', description='Review related options')


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
        except MarshmallowValidationError as err:
            return {'errors': err.messages}, 400
        except (AlreadyExists, NotFound, APIValidationError) as e:
            return {'error': str(e)}, e.status_code


@review_namespace.route('/<uuid:id>/')
class ReviewResource(Resource):
    @inject
    def __init__(self, service: ReviewService, **kwargs):
        super().__init__(**kwargs)
        self._service = service

    @jwt_required()
    def put(self, id: UUID):
        try:
            data = review_update_schema.load(request.get_json())
            updated_review = self._service.update_review(id, data)
            return updated_review, 200
        except MarshmallowValidationError as err:
            return {'errors': err.messages}, 400
        except (NotFound, PermissionDenied, APIValidationError) as e:
            return {'error': str(e)}, e.status_code

    @jwt_required()
    def delete(self, id: UUID):
        try:
            self._service.delete_review(id)
            return '', 204
        except (NotFound, PermissionDenied) as e:
            return {'error': str(e)}, e.status_code


@review_namespace.route('/recipe/<uuid:id>/')
class ReviewByRecipeResource(Resource):
    @inject
    def __init__(self, service: ReviewService, **kwargs):
        super().__init__(**kwargs)
        self._service = service

    def get(self, id: UUID):
        try:
            data = pagination_schema.load(request.args.to_dict())
            page = data.get('page', 1)
            per_page = data.get('per_page', 10)
            reviews = self._service.get_reviews_by_recipe(id, page, per_page)
            return reviews, 200
        except MarshmallowValidationError as ve:
            return {'errors': ve.messages}, 400
        except (NotFound, APIValidationError) as e:
            return {'error': str(e)}, e.status_code


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
        except MarshmallowValidationError as ve:
            return {'errors': ve.messages}, 400
        except (NotFound, APIValidationError) as e:
            return {'error': str(e)}, e.status_code


@review_namespace.route('/<uuid:id>/approve/')
class ApproveReviewResource(Resource):
    @inject
    def __init__(self, service: ReviewService, **kwargs):
        super().__init__(**kwargs)
        self._service = service

    @jwt_required()
    @role_required(['Admin'])
    def patch(self, id: UUID):
        try:
            self._service.approve_review(id)
            return {'message': 'Review approved successfully'}, 200
        except (NotFound, APIValidationError) as e:
            return {'error': str(e)}, e.status_code
