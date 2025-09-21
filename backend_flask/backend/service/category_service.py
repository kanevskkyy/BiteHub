from uuid import UUID
from typing import Optional

from injector import inject
from werkzeug.datastructures import FileStorage

from backend.exceptions import NotFound, AlreadyExists, ValidationError
from backend.helpers.cloudinary_uploader import CloudinaryUploader
from backend.models import Category
from backend.repositories import CategoryRepository
from backend.schemas import categories_schema, category_schema


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
            raise NotFound(f'Cannot find category with id: {id}!')

        return category_schema.dump(category)

    def create(self, data: dict, icon_file: Optional[FileStorage] = None):
        if self.__repository.is_name_exists(data['name']):
            raise AlreadyExists('Category with this name already exists!')

        if not icon_file:
            raise ValidationError('Category needs to have image!')

        category = Category(**data)
        category.icon_url = CloudinaryUploader.upload_file(icon_file, folder='category')

        created_category = self.__repository.create(category)
        return category_schema.dump(created_category)

    def update(self, id: UUID, data: dict, icon_file: Optional[FileStorage] = None):
        category = self.__repository.get_by_id(id)
        if category is None:
            raise NotFound(f'Cannot find category with id: {id}!')

        if self.__repository.is_name_exists(data['name'], id):
            raise AlreadyExists('Category with this name already exists!')

        category.name = data['name']

        if icon_file:
            category.icon_url = CloudinaryUploader.upload_file(icon_file, folder='category')

        updated_category = self.__repository.update(category)
        return category_schema.dump(updated_category)

    def delete(self, id: UUID) -> bool:
        category = self.__repository.get_by_id(id)
        if category is None:
            raise NotFound(f'Cannot find category with id: {id}!')

        if category.icon_url:
            CloudinaryUploader.delete_file(category.icon_url)

        self.__repository.delete(category)

        return True