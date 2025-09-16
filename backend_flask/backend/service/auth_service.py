from typing import Optional

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from injector import inject
from werkzeug.datastructures import FileStorage

from backend import CloudinaryUploader
from backend.models import User
from backend.repositories.role_repository import RoleRepository
from backend.repositories.user_repository import UserRepository


class AuthService:
    @inject
    def __init__(self, repository: UserRepository, role_repository: RoleRepository):
        self.__repository = repository
        self.__role_repository = role_repository

    def register_user(self, data: dict, avatar_file: Optional[FileStorage] = None):
        data.pop('confirm_password', None)

        if self.__repository.is_username_exist(data['username']):
            raise ValueError('User with this username already exists!')

        user = User(**data)
        user.set_password(data['password_hash'])

        role = self.__role_repository.get_role_by_name('User')

        if avatar_file:
            user.avatar_url = CloudinaryUploader.upload_file(avatar_file, folder='users')

        created_user = self.__repository.create(user)

        access_token = create_access_token(identity=created_user.id,
                                           additional_claims={
                                               'role': role.name
                                           })
        refresh_token = create_refresh_token(
            identity=created_user.id,
        )

        return {
            'accessToken': access_token,
            'refreshToken': refresh_token,
        }


    def login_user(self, data: dict) -> dict:
        username = data['username']
        password = data['password']

        user = self.__repository.get_user_by_username(username)
        if user is None:
            raise ValueError('Invalid password or username!')

        if not user.check_password(password):
            raise ValueError('Invalid password or username!')

        access_token = create_access_token(identity=user.id,
                                           additional_claims={
                                               'role': user.role.name
                                           })
        refresh_token = create_refresh_token(
            identity=user.id,
        )

        return {
            'accessToken': access_token,
            'refreshToken': refresh_token,
        }

    def refresh_access_token(self) -> str:
        current_user_id = get_jwt_identity()
        user = self.__repository.get_by_id(current_user_id)
        if not user:
            raise ValueError('Cannot find user with this id')

        access_token = create_access_token(identity=user.id,
                                           additional_claims={
                                               'role': user.role.name
                                           })
        return access_token