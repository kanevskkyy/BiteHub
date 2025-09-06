from flask import Flask
from flask_injector import FlaskInjector
import backend.models
from backend.extensions import db, api
from backend.routes.api_router import APIRouter
from backend.helpers.cloudinary_uploader import CloudinaryUploader
from backend.di import DIConfig
from backend.repositories.category_repository import CategoryRepository
from backend.routes.category_routes import category_namespace, CategoryList
from backend.service.category_service import CategoryService


class AppFactory:
    @staticmethod
    def create_app(app: Flask, extensions: list, config_class) -> Flask:
        app.config.from_object(config_class)

        for init in extensions:
            init(app)

        CloudinaryUploader.init_cloudinary(app)
        APIRouter.register_namespaces(api)
        FlaskInjector(app=app, modules=[DIConfig.configure_repository, DIConfig.configure_services])

        return app