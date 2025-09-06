from flask_restx import Api
from backend.routes.category_routes import category_namespace

class APIRouter:
    @staticmethod
    def register_namespaces(api: Api):
        api.add_namespace(category_namespace, path='/api/categories')