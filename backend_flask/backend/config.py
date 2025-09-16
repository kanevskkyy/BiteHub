from datetime import timedelta

from decouple import config


class Config:
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI', default='sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', default=False, cast=bool)
    CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME', default=None)
    CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY', default=None)
    CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET', default=None)

    JWT_SECRET_KEY = config('JWT_SECRET_KEY', default='secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=config('JWT_ACCESS_TOKEN_EXPIRES', cast=int, default=15)
    )

    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=config('JWT_REFRESH_TOKEN_EXPIRES', cast=int, default=7)
    )

    DEBUG = config('DEBUG', default=True, cast=bool)