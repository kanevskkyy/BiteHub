from typing import Optional
from uuid import UUID

from injector import inject
from werkzeug.datastructures import FileStorage

from backend import CloudinaryUploader
from backend.repositories.user_repository import UserRepository
from backend.schemas.users_schema.user_detail_schema import user_detail_schema


class UserService:
    @inject
    def __init__(self, repository: UserRepository):
        self.__repository = repository

    def get_by_id(self, user_id: UUID) -> dict:
        user = self.__repository.get_by_id(user_id)
        if user is None:
            raise ValueError(f'Cannot find user with id: {user_id}')

        return user_detail_schema.dump(user)

    def update_user(self, user_id: UUID, data: dict, avatar_file: Optional[FileStorage] = None):
        user = self.__repository.get_by_id(user_id)
        if user is None:
            raise ValueError(f'Cannot find user with id: {user_id}')

        if self.__repository.is_username_exist(data['username'], exclude_id=user.id):
            raise ValueError('User with this username already exists!')

        if avatar_file:
            if user.avatar_url:
                CloudinaryUploader.delete_file(user.avatar_url)
            user.avatar_url = CloudinaryUploader.upload_file(avatar_file, folder='users')

        for key, value in data.items():
            setattr(user, key, value)

        self.__repository.update(user)
        return user_detail_schema.dump(user)

    def delete_user(self, user_id: UUID) -> bool:
        user = self.__repository.get_by_id(user_id)
        if user is None:
            raise ValueError(f'Cannot find user with id: {user_id}')

        CloudinaryUploader.delete_file(user.avatar_url)

        return True