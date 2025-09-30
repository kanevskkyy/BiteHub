from injector import Binder, singleton

from backend import CloudinaryUploader
from backend.extensions import db
from backend.repositories import (CategoryRepository, IngredientsRepository,
                                  UserRepository, ReviewRepository,
                                  RecipeRepository, RoleRepository)
from backend.service import (CategoryService, IngredientsService,
                             UserService, AuthService,
                             ReviewService, RecipeService)


class DIConfig:
    """
    Config dependency injection
    """
    @staticmethod
    def configure_repository(binder: Binder):
        binder.bind(db.session.__class__, to=db.session, scope=singleton)
        binder.bind(CategoryRepository, to=CategoryRepository, scope=singleton)
        binder.bind(IngredientsRepository, to=IngredientsRepository, scope=singleton)
        binder.bind(UserRepository, to=UserRepository, scope=singleton)
        binder.bind(ReviewRepository, to=ReviewRepository, scope=singleton)
        binder.bind(RecipeRepository, to=RecipeRepository, scope=singleton)
        binder.bind(RoleRepository, to=RoleRepository, scope=singleton)


    @staticmethod
    def configure_image_service(binder: Binder):
        binder.bind(CloudinaryUploader, to=CloudinaryUploader(), scope=singleton)


    @staticmethod
    def configure_services(binder: Binder):
        binder.bind(CategoryService, to=CategoryService, scope=singleton)
        binder.bind(IngredientsService, to=IngredientsService, scope=singleton)
        binder.bind(UserService, to=UserService, scope=singleton)
        binder.bind(AuthService, to=AuthService, scope=singleton)
        binder.bind(ReviewService, to=ReviewService, scope=singleton)
        binder.bind(RecipeService, to=RecipeService, scope=singleton)