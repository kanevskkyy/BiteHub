from flask import Flask

from flask_injector import FlaskInjector
import backend.models
from backend.extensions import db, api, jwt
from backend.helpers.cloudinary_uploader import CloudinaryUploader
from backend.helpers.uuid_encoder import UUIDEncoder
from backend.routes.api_router import APIRouter
from backend.di import DIConfig


class AppFactory:
    @staticmethod
    def create_app(app: Flask, extensions: list, config_class) -> Flask:
        app.config.from_object(config_class)

        for init in extensions:
            init(app)

        app.json_encoder = UUIDEncoder

        CloudinaryUploader.init_cloudinary(app)
        APIRouter.register_namespaces(api)
        FlaskInjector(app=app, modules=[DIConfig.configure_repository, DIConfig.configure_services])

        return app
