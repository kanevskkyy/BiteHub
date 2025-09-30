from typing import Optional
from uuid import UUID

from flask_jwt_extended import get_jwt_identity
from injector import inject
from werkzeug.datastructures import FileStorage

from backend import CloudinaryUploader
from backend.exceptions import NotFound, PermissionDenied, AlreadyExists
from backend.repositories import UserRepository
from backend.schemas import user_detail_schema


class UserService:
    """
    Service for managing users, including retrieval, updating, and deletion.

    Methods:
        get_by_id(user_id: UUID) -> dict:
            Get user details by ID.

        update_user(user_id: UUID, data: dict, avatar_file: Optional[FileStorage] = None) -> dict:
            Update user information and avatar.
            Only the current user can update their data.

        delete_user(user_id: UUID) -> bool:
            Delete a user. Only the current user can delete themselves.
    """
    @inject
    def __init__(self, repository: UserRepository, cloud_uploader: CloudinaryUploader):
        self.__repository = repository
        self.__cloud_uploader = cloud_uploader

    def get_by_id(self, user_id: UUID) -> dict:
        user = self.__repository.get_by_id(user_id)
        if user is None:
            raise NotFound(f'Cannot find user with id: {user_id}')

        return user_detail_schema.dump(user)

    def update_user(self, user_id: UUID, data: dict, avatar_file: Optional[FileStorage] = None) -> dict:
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
                self.__cloud_uploader.delete_file(user.avatar_url)
            user.avatar_url = self.__cloud_uploader.upload_file(avatar_file, folder='users')

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

        self.__cloud_uploader.delete_file(user.avatar_url)

        return True