from flask_restx import Api

from backend.routes import (ingredient_namespace, category_namespace,
                            user_namespace, auth_namespace, review_namespace,
                            recipe_namespace)


class APIRouter:
    @staticmethod
    def register_namespaces(api: Api):
        api.add_namespace(category_namespace, path='/api/categories')
        api.add_namespace(ingredient_namespace, path='/api/ingredients')
        api.add_namespace(user_namespace, path='/api/users')
        api.add_namespace(auth_namespace, path='/api/auth')
        api.add_namespace(review_namespace, path='/api/reviews')
        api.add_namespace(recipe_namespace, path='/api/recipes')