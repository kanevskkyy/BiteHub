from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

from backend.config import Config

db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title='Backend API',
    version='1.0',
    description='Backend API',
    doc='/docs/',
)
jwt = JWTManager()
limiter = Limiter(
    key_func=lambda: get_jwt_identity() or get_remote_address(),
    storage_uri=Config.REDIS_URL
)