from flask import Flask
import backend.models


class AppFactory:
    @staticmethod
    def create_app(app: Flask, extensions: list, config_class) -> Flask:
        app.config.from_object(config_class)

        for init in extensions:
            init(app)

        return app