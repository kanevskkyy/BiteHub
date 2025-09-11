from uuid import UUID

from injector import inject

from backend.models import Reviews
from backend.repositories.review_repository import ReviewRepository
from backend.schemas.review_schemas.review_schema import review_list_schema, review_schema
from backend.schemas.review_schemas.review_update_schema import review_update_schema


class ReviewService:
    @inject
    def __init__(self, repository: ReviewRepository):
        self.__repository = repository

    def get_reviews_by_recipe(self, recipe_id: UUID, page: int = 1, per_page: int = 10):
        paginated = self.__repository.get_reviews_by_recipe(recipe_id, page, per_page)

        serialized_items = review_list_schema.dump(paginated.items)

        return paginated.to_dict() | {'items': serialized_items}

    def create_review(self, data: dict):
        if self.__repository.is_user_already_rated(data['user_id'], data['recipe_id']):
            raise ValueError('Review already writen by this user!')

        review = Reviews(**data)
        created_review = self.__repository.create(review)

        return review_schema.dump(created_review)

    def update_review(self, review_id: UUID, data: dict) -> dict:
        review = self.__repository.get_by_id(review_id)

        if review is None:
            raise ValueError('Review does not exist!')

        for key, value in data.items():
            setattr(review, key, value)

        self.__repository.update(review)

        return review_schema.dump(review)

    def delete_review(self, review_id: UUID) -> bool:
        review = self.__repository.get_by_id(review_id)

        if review is None:
            raise ValueError('Review does not exist!')

        self.__repository.delete(review)

        return True