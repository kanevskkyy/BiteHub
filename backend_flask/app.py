from flask import Flask

from backend import AppFactory
from backend.config import Config
from backend.extensions import db, migrate

app = AppFactory.create_app(
    Flask(__name__),
    extensions=[
        lambda factory: db.init_app(factory),
        lambda factory: migrate.init_app(factory, db)
    ],
    config_class=Config
)

if __name__ == '__main__':
    app.run()