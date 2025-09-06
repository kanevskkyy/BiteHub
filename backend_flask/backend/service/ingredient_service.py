from typing import Optional
from uuid import UUID

from injector import inject
from werkzeug.datastructures import FileStorage

from backend.helpers.cloudinary_uploader import CloudinaryUploader
from backend.repositories.ingredients_repository import IngredientsRepository
from backend.schemas.ingredient_schema import ingredients_schema, ingredient_schema


class IngredientsService:
    @inject
    def __init__(self, repository: IngredientsRepository):
        self.__repository = repository

    def get_all(self):
        ingredients = self.__repository.get_all()
        return ingredients_schema.dump(ingredients)

    def get_by_id(self, id: UUID):
        ingredient = self.__repository.get_by_id(id)
        if ingredient is None:
            raise ValueError(f'Cannot find ingredient with id: {id}!')
        return ingredient_schema.dump(ingredient)

    def create(self, data: dict, icon_file: Optional[FileStorage] = None):
        ingredient = ingredient_schema.load(data)

        if self.__repository.is_name_exists(ingredient.name):
            raise ValueError('Ingredient with this name already exists!')

        if icon_file:
            ingredient.icon_url = CloudinaryUploader.upload_file(icon_file, folder='ingredients')
        else:
            raise ValueError('Ingredient needs to have an image!')

        created_ingredient = self.__repository.create(ingredient)
        return ingredient_schema.dump(created_ingredient)


    def update(self, id: UUID, data: dict, icon_file: Optional[FileStorage] = None):
        ingredient = self.__repository.get_by_id(id)
        if ingredient is None:
            raise ValueError(f'Cannot find ingredient with id: {id}!')

        validated_ingredient = ingredient_schema.load(data)

        if self.__repository.is_name_exists(validated_ingredient.name, id):
            raise ValueError('Ingredient with this name already exists!')

        ingredient.name = validated_ingredient.name
        if icon_file:
            ingredient.icon_url = CloudinaryUploader.upload_file(icon_file, folder='ingredients')

        updated_ingredient = self.__repository.update(ingredient)
        return ingredient_schema.dump(updated_ingredient)


    def delete(self, id: UUID) -> bool:
        ingredient = self.__repository.get_by_id(id)
        if ingredient is None:
            raise ValueError(f'Cannot find ingredient with id: {id}!')

        if ingredient.icon_url:
            CloudinaryUploader.delete_file(ingredient.icon_url)

        self.__repository.delete(ingredient)

        return True