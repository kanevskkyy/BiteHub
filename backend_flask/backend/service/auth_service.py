from typing import Optional

from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity
from injector import inject
from werkzeug.datastructures import FileStorage

from backend import CloudinaryUploader
from backend.models import User, RefreshToken
from backend.exceptions import AlreadyExists, NotFound, ValidationError
from backend.repositories import UserRepository, RoleRepository, RefreshTokenRepository
from backend.schemas.auth.token_schema import token_schema


class AuthService:
    """
    Service for handling authentication and user-related operations.

    Methods:
        check_username_exist(username): Check if a username already exists.
        register_user(data, avatar_file): Register a new user.
        login_user(data): Authenticate a user and return JWT tokens.
        refresh_access_token(): Refresh JWT access token.
        change_password(data): Change current user's password.
     """

    @inject
    def __init__(self, user_repository: UserRepository, role_repository: RoleRepository,
                 cloud_uploader: CloudinaryUploader, refresh_token_repository: RefreshTokenRepository):
        self.__user_repository = user_repository
        self.__role_repository = role_repository
        self.__cloud_uploader = cloud_uploader
        self.__refresh_token_repository = refresh_token_repository

    def check_username_exist(self, username) -> dict:
        exist = self.__user_repository.is_username_exist(username)
        return {
            'exists': exist
        }


    def register_user(self, data: dict, avatar_file: Optional[FileStorage] = None) -> dict:
        data.pop('confirm_password', None)

        if self.__user_repository.is_username_exist(data['username']):
            raise AlreadyExists('User with this username already exists!')

        user = User(**data)
        user.set_password(data['password_hash'])

        role = self.__role_repository.get_role_by_name('User')
        if role is None:
            raise NotFound('Role "User" not found in DB!')

        user.role_id = role.id

        if avatar_file:
            user.avatar_url = self.__cloud_uploader.upload_file(avatar_file, folder='users')

        created_user = self.__user_repository.create(user)

        access_token = create_access_token(
            identity=created_user.id,
            additional_claims={
                'role': role.name
            }
        )
        refresh_token = create_refresh_token(
            identity=created_user.id
        )

        refresh_token_obj = RefreshToken(user_id=created_user.id, token=refresh_token)
        self.__refresh_token_repository.create(refresh_token_obj)

        return token_schema.dump(
            {
                'accessToken': access_token,
                'refreshToken': refresh_token
             }
        )

    def login_user(self, data: dict) -> dict:
        username = data['username']
        password = data['password']

        user = self.__user_repository.get_user_by_username(username)
        if not user or not user.check_password(password):
            raise ValidationError('Invalid username or password!')

        access_token = create_access_token(
            identity=user.id,
            additional_claims={
                'role': user.role.name
            }
        )

        refresh_token = create_refresh_token(identity=user.id)
        refresh_token_obj = RefreshToken(user_id=user.id, token=refresh_token)
        self.__refresh_token_repository.create(refresh_token_obj)

        return token_schema.dump({'accessToken': access_token, 'refreshToken': refresh_token})

    def refresh_access_token(self, refresh_token: str) -> str:
        token_in_db = self.__refresh_token_repository.get_by_token(refresh_token)
        if not token_in_db:
            raise ValidationError('Invalid refresh token!')

        user = self.__user_repository.get_by_id(token_in_db.user_id)
        if not user:
            raise NotFound('Cannot find user with this id')

        access_token = create_access_token(
            identity=user.id,
            additional_claims={'role': user.role.name}
        )
        return access_token

    def change_password(self, data: dict) -> bool:
        current_user_id = get_jwt_identity()
        user = self.__user_repository.get_by_id(current_user_id)
        if not user:
            raise NotFound('Cannot find user with this id')

        if not user.check_password(data['old_password']):
            raise ValidationError('Old password is incorrect!')

        if user.check_password(data['new_password']):
            raise ValidationError('New password cannot be the same as the old password!')

        user.set_password(data['new_password'])
        self.__user_repository.update(user)
        return True

    def logout_user(self) -> bool:
        current_user_id = get_jwt_identity()
        self.__refresh_token_repository.delete_by_user_id(current_user_id)
        return True