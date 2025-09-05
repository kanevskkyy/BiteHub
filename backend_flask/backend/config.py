from decouple import config


class Config:
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI', default='sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS', default=False, cast=bool)

    DEBUG = config('DEBUG', default=True, cast=bool)