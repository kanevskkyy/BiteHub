from typing import Optional, List
from uuid import UUID

from injector import inject
from werkzeug.datastructures import FileStorage

from backend.exceptions import NotFound, AlreadyExists, ValidationError
from backend.helpers.cloudinary_uploader import CloudinaryUploader
from backend.models import Ingredients
from backend.repositories import IngredientsRepository
from backend.schemas import ingredients_schema, ingredient_schema


class IngredientsService:
    """
    Service for managing ingredients, including CRUD operations
    and handling image uploads via Cloudinary.

    Methods:
        get_all(): Return a list of all ingredients.
        get_by_id(id): Return a single ingredient by its UUID.
        create(data, icon_file): Create a new ingredient with an image.
        update(id, data, icon_file): Update an existing ingredient and optionally its image.
        delete(id): Delete an ingredient and remove its associated image.
    """

    @inject
    def __init__(self, repository: IngredientsRepository, cloud_uploader: CloudinaryUploader):
        self.__repository = repository
        self.__cloud_uploader = cloud_uploader

    def get_all(self) -> List[dict]:
        ingredients = self.__repository.get_all()
        return ingredients_schema.dump(ingredients)

    def get_by_id(self, id: UUID) -> dict:
        ingredient = self.__repository.get_by_id(id)
        if ingredient is None:
            raise NotFound(f'Cannot find ingredient with id: {id}!')
        return ingredient_schema.dump(ingredient)

    def create(self, data: dict, icon_file: Optional[FileStorage] = None) -> dict:
        if self.__repository.is_name_exists(data['name']):
            raise AlreadyExists('Ingredient with this name already exists!')

        if not icon_file:
            raise ValidationError('Ingredient needs to have an image!')

        ingredient = Ingredients(**data)
        ingredient.icon_url = self.__cloud_uploader.upload_file(icon_file, folder='ingredients')

        created_ingredient = self.__repository.create(ingredient)
        return ingredient_schema.dump(created_ingredient)

    def update(self, id: UUID, data: dict, icon_file: Optional[FileStorage] = None) -> dict:
        ingredient = self.__repository.get_by_id(id)
        if ingredient is None:
            raise NotFound(f'Cannot find ingredient with id: {id}!')

        if self.__repository.is_name_exists(data['name'], id):
            raise AlreadyExists('Ingredient with this name already exists!')

        ingredient.name = data['name']

        if icon_file:
            ingredient.icon_url = self.__cloud_uploader.upload_file(icon_file, folder='ingredients')

        updated_ingredient = self.__repository.update(ingredient)
        return ingredient_schema.dump(updated_ingredient)

    def delete(self, id: UUID) -> bool:
        ingredient = self.__repository.get_by_id(id)
        if ingredient is None:
            raise NotFound(f'Cannot find ingredient with id: {id}!')

        if ingredient.icon_url:
            self.__cloud_uploader.delete_file(ingredient.icon_url)

        self.__repository.delete(ingredient)
        return True