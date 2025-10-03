from unittest.mock import Mock, MagicMock

import pytest
from flask import Flask
from sqlalchemy.orm import scoped_session, sessionmaker

from backend import AppFactory
from backend.extensions import db, migrate, api, jwt, limiter
from backend.repositories import RoleRepository
from backend.service import CategoryService, IngredientsService, ReviewService, RecipeService, UserService, AuthService
from tests.test_config import TestConfig


@pytest.fixture(scope='session')
def app():
    app = AppFactory.create_app(
        Flask(__name__),
        extensions=[
            lambda factory: db.init_app(factory),
            lambda factory: migrate.init_app(factory, db),
            lambda factory: api.init_app(factory),
            lambda factory: jwt.init_app(factory),
            lambda factory: limiter.init_app(factory),
        ],
        config_class=TestConfig,
    )
    return app


@pytest.fixture(scope='session')
def db_instance(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.drop_all()


@pytest.fixture(scope='function')
def db_session(app, db_instance):
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()

        session_factory = sessionmaker(bind=connection)
        session = scoped_session(session_factory)

        old_session = db.session
        db.session = session

        yield session

        session.close()
        transaction.rollback()
        connection.close()

        db.session = old_session


@pytest.fixture
def mock_role_repo():
    return MagicMock(spec=RoleRepository)

@pytest.fixture
def mock_user_repo():
    return Mock()

@pytest.fixture
def mock_repo():
    return Mock()

@pytest.fixture
def mock_uploader():
    return Mock()

@pytest.fixture
def mock_review_repo():
    return Mock()

@pytest.fixture
def category_service(mock_repo, mock_uploader):
    return CategoryService(repository=mock_repo, cloud_uploader=mock_uploader)

@pytest.fixture
def ingredients_service(mock_repo, mock_uploader):
    return IngredientsService(repository=mock_repo, cloud_uploader=mock_uploader)

@pytest.fixture
def review_service(mock_repo, mock_role_repo):
    return ReviewService(mock_repo, mock_role_repo)

@pytest.fixture
def recipe_service(mock_repo, mock_review_repo, mock_uploader):
    return RecipeService(repository=mock_repo, review_repo=mock_review_repo, cloud_uploader=mock_uploader)

@pytest.fixture
def user_service(mock_repo, mock_uploader):
    return UserService(repository=mock_repo, cloud_uploader=mock_uploader)

@pytest.fixture
def auth_service(mock_user_repo, mock_role_repo, mock_uploader):
    return AuthService(
        user_repository=mock_user_repo,
        role_repository=mock_role_repo,
        cloud_uploader=mock_uploader
    )