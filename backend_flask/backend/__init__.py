import json

from flask import Flask
from flask_cors import CORS

from flask_injector import FlaskInjector

import backend.models
from backend.extensions import db, api, jwt
from backend.helpers.cloudinary_uploader import CloudinaryUploader
from backend.helpers.error_handler import ErrorHandlerConfigurator
from backend.helpers.json_encoder import UUIDJSONEncoder
from backend.routes.api_router import APIRouter
from backend.di import DIConfig


class AppFactory:
    @staticmethod
    def _configure_json_encoding(app: Flask) -> None:
        app.json_encoder = UUIDJSONEncoder
        api.representations['application/json'] = lambda data, code, headers=None: \
            app.make_response((json.dumps(data, cls=UUIDJSONEncoder, ensure_ascii=False) + '\n',
                               code, headers))

    @staticmethod
    def _configure_error_handlers(api):
        ErrorHandlerConfigurator.init(api)

    @staticmethod
    def _configure_extensions(app: Flask, extensions: list) -> None:
        for init in extensions:
            init(app)

    @staticmethod
    def _configure_services(app: Flask) -> None:
        CloudinaryUploader.init_cloudinary(app)
        APIRouter.register_namespaces(api)
        FlaskInjector(app=app, modules=[DIConfig.configure_repository, DIConfig.configure_services])
        CORS(app, resources={r'/api/*': {'origins': app.config['CORS_ORIGINS']}})

    @staticmethod
    def create_app(app: Flask, extensions: list, config_class) -> Flask:
        app.config.from_object(config_class)

        AppFactory._configure_extensions(app, extensions)
        AppFactory._configure_json_encoding(app)
        AppFactory._configure_services(app)
        AppFactory._configure_error_handlers(api)

        return app