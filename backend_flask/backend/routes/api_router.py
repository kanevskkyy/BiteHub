from flask_restx import Api

from backend.routes.ingredient_routes import ingredient_namespace


class APIRouter:
    @staticmethod
    def register_namespaces(api: Api):
        from backend.routes.category_routes import category_namespace

        api.add_namespace(category_namespace, path='/api/categories')
        api.add_namespace(ingredient_namespace, path='/api/ingredients')