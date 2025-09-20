from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
api = Api(
    title='Backend API',
    version='1.0',
    description='Backend API',
    doc='/docs/',
)
jwt = JWTManager()