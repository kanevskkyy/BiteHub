from backend.config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    TESTING = True
    DEBUG = False