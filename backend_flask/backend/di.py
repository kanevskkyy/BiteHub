from injector import Binder, singleton

from backend.extensions import db
from backend.repositories.category_repository import CategoryRepository
from backend.repositories.ingredients_repository import IngredientsRepository
from backend.service.category_service import CategoryService
from backend.service.ingredient_service import IngredientsService


class DIConfig:
    @staticmethod
    def configure_repository(binder: Binder):
        binder.bind(db.session.__class__, to=db.session, scope=singleton)
        binder.bind(CategoryRepository, to=CategoryRepository, scope=singleton)
        binder.bind(IngredientsRepository, to=IngredientsRepository, scope=singleton)

    @staticmethod
    def configure_services(binder: Binder):
        binder.bind(CategoryService, to=CategoryService, scope=singleton)
        binder.bind(IngredientsService, to=IngredientsService, scope=singleton)