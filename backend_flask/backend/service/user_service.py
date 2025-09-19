from typing import Optional
from uuid import UUID

from flask_jwt_extended import get_jwt_identity
from injector import inject
from werkzeug.datastructures import FileStorage

from backend import CloudinaryUploader
from backend.exceptions import NotFound, PermissionDenied, AlreadyExists
from backend.repositories.user_repository import UserRepository
from backend.schemas.users_schema.user_detail_schema import user_detail_schema


class UserService:
    @inject
    def __init__(self, repository: UserRepository):
        self.__repository = repository

    def get_by_id(self, user_id: UUID) -> dict:
        user = self.__repository.get_by_id(user_id)
        if user is None:
            raise NotFound(f'Cannot find user with id: {user_id}')

        return user_detail_schema.dump(user)

    def update_user(self, user_id: UUID, data: dict, avatar_file: Optional[FileStorage] = None):
        current_user_id = get_jwt_identity()

        user = self.__repository.get_by_id(user_id)
        if user is None:
            raise NotFound(f'Cannot find user with id: {user_id}')

        if user.id != current_user_id:
            raise PermissionDenied(f'You don`t have permission to update this user')

        if self.__repository.is_username_exist(data['username'], exclude_id=user.id):
            raise AlreadyExists('User with this username already exists!')

        if avatar_file:
            if user.avatar_url:
                CloudinaryUploader.delete_file(user.avatar_url)
            user.avatar_url = CloudinaryUploader.upload_file(avatar_file, folder='users')

        for key, value in data.items():
            setattr(user, key, value)

        self.__repository.update(user)
        return user_detail_schema.dump(user)

    def delete_user(self, user_id: UUID) -> bool:
        current_user_id = get_jwt_identity()
        user = self.__repository.get_by_id(user_id)

        if user is None:
            raise NotFound(f'Cannot find user with id: {user_id}')

        if user.id != current_user_id:
            raise PermissionDenied(f'You don`t have permission to delete this user')

        CloudinaryUploader.delete_file(user.avatar_url)

        return True