from marshmallow import Schema, fields


class RecipeListSchema(Schema):
    id = fields.UUID(dump_only=True, required=True)
    title = fields.String(dump_only=True, required=True)
    description = fields.String(dump_only=True, required=True)
    servings_count = fields.Integer(dump_only=True, data_key='servingsCount')
    duration = fields.Integer(required=True, dump_only=True)

    ingredients = fields.Method('get_ingredients')
    categories = fields.Method('get_categories')

    review_count = fields.Integer(dump_only=True, data_key='reviewCount')
    average_rating = fields.Float(dump_only=True, data_key='averageRating')

    def get_ingredients(self, obj):
        if hasattr(obj, 'recipe_ingredients'):
            return [
                {'id': ri.ingredient.id, 'name': ri.ingredient.name}
                for ri in obj.recipe_ingredients
            ]
        return []

    def get_categories(self, obj):
        if hasattr(obj, 'recipe_categories'):
            return [
                {'id': rc.category.id, 'name': rc.category.name}
                for rc in obj.recipe_categories
            ]
        return []


recipe_list_schema = RecipeListSchema(many=True)