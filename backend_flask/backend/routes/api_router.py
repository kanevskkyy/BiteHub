from flask_restx import Api

from backend.routes.auth_routes import auth_namespace
from backend.routes.ingredient_routes import ingredient_namespace
from backend.routes.category_routes import category_namespace
from backend.routes.recipe_routes import recipe_namespace
from backend.routes.review_routes import review_namespace
from backend.routes.user_routes import user_namespace


class APIRouter:
    @staticmethod
    def register_namespaces(api: Api):
        api.add_namespace(category_namespace, path='/api/categories')
        api.add_namespace(ingredient_namespace, path='/api/ingredients')
        api.add_namespace(user_namespace, path='/api/users')
        api.add_namespace(auth_namespace, path='/api/auth')
        api.add_namespace(review_namespace, path='/api/reviews')
        api.add_namespace(recipe_namespace, path='/api/recipes')