from typing import Optional

from injector import inject
from werkzeug.datastructures import FileStorage

from backend import CloudinaryUploader
from backend.models import User
from backend.repositories.user_repository import UserRepository


class AuthService:
    @inject
    def __init__(self, repository: UserRepository):
        self.__repository = repository

    def register_user(self, data: dict, avatar_file: Optional[FileStorage] = None):
        data.pop('confirm_password', None)

        if self.__repository.is_username_exist(data['username']):
            raise ValueError('User with this username already exists!')

        user = User(**data)
        user.set_password(data['password_hash'])


        if avatar_file:
            user.avatar_url = CloudinaryUploader.upload_file(avatar_file)

        self.__repository.create(user)

        return {
            'accessToken': 'here will be access token',
            'refreshToken': 'here will be refresh token',
        }