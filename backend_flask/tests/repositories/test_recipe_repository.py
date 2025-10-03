from backend.models import Role, User, Recipe, Ingredient, Category
from backend.repositories import RoleRepository, UserRepository, RecipeRepository, IngredientRepository, \
    CategoryRepository


def test_create_recipe_with_role(db_session):
    role_repo = RoleRepository()
    role = Role(name='User')
    role_repo.create(role)

    user_repo = UserRepository()
    user = User(
        username='test_user',
        password_hash='hashed_pw',
        first_name='Test',
        last_name='User',
        role_id=role.id
    )
    user_repo.create(user)

    recipe_repo = RecipeRepository()
    recipe = Recipe(
        title='Test Recipe',
        description='Test Description',
        duration=30,
        servings_count=2,
        author_id=user.id
    )
    created = recipe_repo.create(recipe)

    assert created.id is not None
    assert created.title == 'Test Recipe'
    assert created.author_id == user.id


def test_is_recipe_title_for_user_exists(db_session):
    role_repo = RoleRepository()
    role = Role(name='User')
    role_repo.create(role)

    user_repo = UserRepository()
    user = User(
        username='another_user',
        password_hash='hashed_pw',
        first_name='Another',
        last_name='User',
        role_id=role.id
    )
    user_repo.create(user)

    recipe_repo = RecipeRepository()
    recipe = Recipe(
        title='Unique Recipe',
        description='Desc',
        duration=10,
        servings_count=1,
        author_id=user.id
    )
    recipe_repo.create(recipe)

    assert recipe_repo.is_recipe_title_for_user_exists('Unique Recipe', user.id) is True
    assert recipe_repo.is_recipe_title_for_user_exists('Other Recipe', user.id) is False


def test_update_recipe_relations(db_session):
    role_repo = RoleRepository()
    role = Role(name='Chef')
    role_repo.create(role)

    user_repo = UserRepository()
    user = User(
        username='chef_user',
        password_hash='hashed_pw',
        first_name='Chef',
        last_name='User',
        role_id=role.id
    )
    user_repo.create(user)

    recipe_repo = RecipeRepository()
    recipe = Recipe(
        title='Test Recipe',
        description='Test Description',
        duration=20,
        servings_count=2,
        author_id=user.id
    )
    recipe_repo.create(recipe)

    ingredient_repo = IngredientRepository()
    ing1 = ingredient_repo.create(Ingredient(name='Salt', icon_url='https://salt.jpg'))
    ing2 = ingredient_repo.create(Ingredient(name='Pepper', icon_url='https://pepper.jpg'))

    category_repo = CategoryRepository()
    cat1 = category_repo.create(Category(name='Soup', icon_url='https://soup.jpg'))
    cat2 = category_repo.create(Category(name='Spicy', icon_url='https://spicy.jpg'))

    steps_data = [
        {'step_number': 1, 'description': 'Boil water'},
        {'step_number': 2, 'description': 'Add salt'}
    ]
    recipe_repo.update_steps(recipe, steps_data)
    db_session.commit()

    assert len(recipe.steps) == 2
    assert recipe.steps[0].description == 'Boil water'

    recipe_repo.update_ingredients(recipe, [ing1.id, ing2.id])
    db_session.commit()

    ingredient_ids_in_recipe = [ri.ingredient_id for ri in recipe.recipe_ingredients]
    assert set(ingredient_ids_in_recipe) == {ing1.id, ing2.id}

    recipe_repo.update_categories(recipe, [cat1.id, cat2.id])
    db_session.commit()

    category_ids_in_recipe = [rc.category_id for rc in recipe.recipe_categories]
    assert set(category_ids_in_recipe) == {cat1.id, cat2.id}

    steps_data_updated = [
        {'id': recipe.steps[0].id, 'step_number': 1, 'description': 'Boil water again'}
    ]
    recipe_repo.update_steps(recipe, steps_data_updated)
    recipe_repo.update_ingredients(recipe, [ing1.id])
    recipe_repo.update_categories(recipe, [cat1.id])
    db_session.commit()

    assert len(recipe.steps) == 1
    assert recipe.steps[0].description == 'Boil water again'
    assert len(recipe.recipe_ingredients) == 1
    assert recipe.recipe_ingredients[0].ingredient_id == ing1.id
    assert len(recipe.recipe_categories) == 1
    assert recipe.recipe_categories[0].category_id == cat1.id