from typing import Optional
from uuid import UUID

from injector import inject
from werkzeug.datastructures import FileStorage
from backend.helpers.cloudinary_uploader import CloudinaryUploader
from backend.repositories.category_repository import CategoryRepository
from backend.schemas.category_schema import categories_schema, category_schema


class CategoryService:
    @inject
    def __init__(self, repository: CategoryRepository):
        self.__repository = repository

    def get_all(self):
        categories = self.__repository.get_all()
        return categories_schema.dump(categories)

    def get_by_id(self, id: UUID):
        category = self.__repository.get_by_id(id)
        if category is None:
            raise ValueError(f'Cannot find category with id: {id}!')

        return category_schema.dump(category)

    def create(self, data: dict, icon_file: Optional[FileStorage] = None):
        category = category_schema.load(data)

        if self.__repository.is_name_exists(category.name):
            raise ValueError('Category with this name already exists!')

        if icon_file:
            category.icon_url = CloudinaryUploader.upload_file(icon_file, folder='category')
        else:
            raise ValueError('Category need to have image!')

        created_category = self.__repository.create(category)
        return category_schema.dump(created_category)

    def update(self, id: UUID, data: dict, icon_file: Optional[FileStorage] = None):
        category = self.__repository.get_by_id(id)
        validated_category = category_schema.load(data)
        if category is None:
            raise ValueError(f'Cannot find category with id: {id}!')

        if self.__repository.is_name_exists(validated_category.name, id):
            raise ValueError('Category with this name already exists!')

        category.name = validated_category.name
        if icon_file:
            category.icon_url = CloudinaryUploader.upload_file(icon_file, folder='category')
        else:
            raise ValueError('Category need to have image!')

        category = self.__repository.update(category)
        return category_schema.dump(category)

    def delete(self, id: UUID) -> bool:
        category = self.__repository.get_by_id(id)
        if category is None:
            raise ValueError(f'Cannot find category with id: {id}!')

        if category.icon_url:
            CloudinaryUploader.delete_file(category.icon_url)

        self.__repository.delete(category)

        return True