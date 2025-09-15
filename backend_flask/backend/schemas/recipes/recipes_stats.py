from dataclasses import dataclass
from typing import Any


@dataclass
class RecipeWithStats:
    recipe: Any
    review_count: int
    average_rating: float

    @property
    def id(self):
        return self.recipe.id

    @property
    def title(self):
        return self.recipe.title

    @property
    def description(self):
        return self.recipe.description

    @property
    def servings_count(self):
        return self.recipe.servings_count

    @property
    def duration(self):
        return self.recipe.duration

    @property
    def recipe_ingredients(self):
        return self.recipe.recipe_ingredients

    @property
    def recipe_categories(self):
        return self.recipe.recipe_categories