from flask import Flask
from backend import AppFactory
from backend.config import Config
from backend.extensions import db, migrate, api, jwt

app = AppFactory.create_app(
    Flask(__name__),
    extensions=[
        lambda factory: db.init_app(factory),
        lambda factory: migrate.init_app(factory, db),
        lambda factory: api.init_app(factory),
        lambda factory: jwt.init_app(factory),
    ],
    config_class=Config
)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
