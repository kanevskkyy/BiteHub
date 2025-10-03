from backend.models import Ingredient
from backend.repositories import IngredientRepository


def test_create_ingredient(db_session):
    repo = IngredientRepository()
    ingredient = Ingredient(name='test_ingredient', icon_url='https://test.jpg')
    ingredient = repo.create(ingredient)

    found = repo.get_by_id(ingredient.id)

    assert found is not None
    assert found.name == 'test_ingredient'
    assert found.icon_url == 'https://test.jpg'


def test_get_all_ingredients(db_session):
    repo = IngredientRepository()
    ingredients = repo.get_all()

    assert ingredients == []

    ingredient1 = Ingredient(name='test_ingredient1', icon_url='https://test1.jpg')
    ingredient2 = Ingredient(name='test_ingredient2', icon_url='https://test2.jpg')
    repo.create(ingredient1)
    repo.create(ingredient2)

    ingredients = repo.get_all()

    assert ingredients is not None
    assert len(ingredients) == 2
    assert ingredients[0].name == 'test_ingredient1'
    assert ingredients[1].name == 'test_ingredient2'


def test_update_ingredient(db_session):
    repo = IngredientRepository()

    ingredient = Ingredient(name='test_ingredient', icon_url='https://test1.jpg')
    ingredient = repo.create(ingredient)

    assert repo.get_by_id(ingredient.id) is not None

    ingredient.name = 'updated_name'
    ingredient = repo.update(ingredient)

    assert repo.get_by_id(ingredient.id) is not None
    assert ingredient.name == 'updated_name'


def test_delete_ingredient(db_session):
    repo = IngredientRepository()
    ingredient = Ingredient(name='test_ingredient', icon_url='https://test1.jpg')

    ingredient = repo.create(ingredient)

    assert repo.get_by_id(ingredient.id) is not None

    repo.delete(ingredient)

    assert repo.get_by_id(ingredient.id) is None


def test_is_name_exists(db_session):
    repo = IngredientRepository()

    ingredient = Ingredient(name='unique_ingredient', icon_url='https://test.jpg')
    ingredient = repo.create(ingredient)

    assert repo.is_name_exists('unique_ingredient') is True
    assert repo.is_name_exists('non_existent') is False

    assert repo.is_name_exists('unique_ingredient', exclude_id=ingredient.id) is False