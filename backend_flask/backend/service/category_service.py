from uuid import UUID
from typing import Optional, List

from injector import inject
from werkzeug.datastructures import FileStorage

from backend import CloudinaryUploader
from backend.exceptions import NotFound, AlreadyExists, ValidationError
from backend.models import Category
from backend.repositories import CategoryRepository
from backend.schemas import categories_schema, category_schema


class CategoryService:
    """
    Service for managing categories, including CRUD operations
    and handling image uploads via Cloudinary.

    Methods:
        get_all(): Return a list of all categories.
        get_by_id(id): Return a single category by its UUID.
        create(data, icon_file): Create a new category with an image.
        update(id, data, icon_file): Update an existing category and optionally its image.
        delete(id): Delete a category and remove its associated image.
    """

    @inject
    def __init__(self, repository: CategoryRepository, cloud_uploader: CloudinaryUploader):
        self.__repository = repository
        self.__cloud_uploader = cloud_uploader

    def get_all(self) -> List[dict]:
        categories = self.__repository.get_all()
        return categories_schema.dump(categories)

    def get_by_id(self, id: UUID) -> dict:
        category = self.__repository.get_by_id(id)
        if category is None:
            raise NotFound(f'Cannot find category with id: {id}!')

        return category_schema.dump(category)

    def create(self, data: dict, icon_file: Optional[FileStorage] = None) -> dict:
        if self.__repository.is_name_exists(data['name']):
            raise AlreadyExists('Category with this name already exists!')

        if not icon_file:
            raise ValidationError('Category needs to have image!')

        category = Category(**data)
        category.icon_url = self.__cloud_uploader.upload_file(icon_file, folder='category')

        created_category = self.__repository.create(category)
        return category_schema.dump(created_category)

    def update(self, id: UUID, data: dict, icon_file: Optional[FileStorage] = None) -> dict:
        category = self.__repository.get_by_id(id)
        if category is None:
            raise NotFound(f'Cannot find category with id: {id}!')

        if self.__repository.is_name_exists(data['name'], id):
            raise AlreadyExists('Category with this name already exists!')

        category.name = data['name']

        if icon_file:
            category.icon_url = self.__cloud_uploader.upload_file(icon_file, folder='category')

        updated_category = self.__repository.update(category)
        return category_schema.dump(updated_category)

    def delete(self, id: UUID) -> bool:
        category = self.__repository.get_by_id(id)
        if category is None:
            raise NotFound(f'Cannot find category with id: {id}!')

        if category.icon_url:
            self.__cloud_uploader.delete_file(category.icon_url)

        self.__repository.delete(category)

        return True