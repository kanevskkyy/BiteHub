from injector import singleton, Binder
from backend import db, CategoryRepository, CategoryService


class DIConfig:
    @staticmethod
    def configure_repository(binder: Binder):
        binder.bind(db.session.__class__, to=db.session, scope=singleton)
        binder.bind(CategoryRepository, to=CategoryRepository, scope=singleton)

    @staticmethod
    def configure_services(binder: Binder):
        binder.bind(CategoryService, to=CategoryService, scope=singleton)
