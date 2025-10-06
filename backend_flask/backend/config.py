from datetime import timedelta

from decouple import config


class Config:
    """
    Base configuration for the Flask application.

    Contains:
        - Database URI and SQLAlchemy settings
        - Cloudinary credentials
        - JWT settings (secret key, expiration times, issuer/audience)
        - Debug mode
        - CORS allowed origins
    """
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
    JWT_ENCODE_ISSUER = config('JWT_ENCODE_ISSUER', default=None)
    JWT_DECODE_ISSUER = config('JWT_DECODE_ISSUER', default=None)
    JWT_DECODE_AUDIENCE = config('JWT_DECODE_AUDIENCE', default=None)

    DEBUG = config('DEBUG', default=True, cast=bool)

    CORS_ORIGINS = config('ALLOWED_ORIGIN', default='*')
    REDIS_URL = config('REDIS_URL', default='redis://localhost:6379')