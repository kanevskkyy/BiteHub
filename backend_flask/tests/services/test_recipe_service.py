from uuid import uuid4
from unittest.mock import patch
import pytest
from werkzeug.datastructures import FileStorage
from backend.models import Recipe, RecipeStep, RecipeIngredient, RecipeCategory


def test_get_recipe_by_id_found(recipe_service, mock_repo, mock_review_repo):
    recipe = Recipe(title='Test', description='Desc', duration=10, servings_count=2, author_id=uuid4())
    recipe.id = uuid4()
    mock_repo.get_by_id.return_value = recipe
    mock_review_repo.has_any_review.return_value = True
    mock_review_repo.has_approved_review.return_value = False

    with patch('backend.service.recipe_service.get_jwt_identity', return_value=str(recipe.author_id)):
        result = recipe_service.get_recipe_by_id(recipe.id)

    assert result['title'] == 'Test'
    assert result['isReviewed'] is True
    assert result['isApprovedReview'] is False
    mock_repo.get_by_id.assert_called_once_with(recipe.id)


def test_get_recipe_by_id_not_found(recipe_service, mock_repo):
    mock_repo.get_by_id.return_value = None
    recipe_id = uuid4()

    with pytest.raises(Exception):
        recipe_service.get_recipe_by_id(recipe_id)


def test_create_recipe_success(recipe_service, mock_repo, mock_uploader):
    user_id = uuid4()
    step = RecipeStep(step_number=1, description='Step1')
    ingredient_id = uuid4()
    category_id = uuid4()

    data = {
        'title': 'New Recipe',
        'description': 'Desc',
        'duration': 15,
        'servings_count': 2,
        'steps': [{'step_number': 1, 'description': 'Step1'}],
        'ingredients_ids': [ingredient_id],
        'category_ids': [category_id]
    }

    file = FileStorage(filename='image.jpg')

    mock_repo.create.return_value = Recipe(
        title='New Recipe',
        description='Desc',
        duration=15,
        servings_count=2,
        author_id=user_id,
        image_url='uploaded_url',
        steps=[step],
        recipe_ingredients=[RecipeIngredient(ingredient_id=ingredient_id)],
        recipe_categories=[RecipeCategory(category_id=category_id)]
    )

    mock_uploader.upload_file.return_value = 'uploaded_url'

    with patch('backend.service.recipe_service.get_jwt_identity', return_value=user_id):
        result = recipe_service.create(data, file)

    assert result['title'] == 'New Recipe'
    mock_uploader.upload_file.assert_called_once_with(file, folder='recipes')
    mock_repo.create.assert_called_once()


def test_update_recipe_success(recipe_service, mock_repo, mock_uploader):
    user_id = uuid4()
    recipe = Recipe(title='Old', description='Desc', duration=10, servings_count=1, author_id=user_id)
    recipe.id = uuid4()
    mock_repo.get_by_id.return_value = recipe
    mock_repo.update.return_value = recipe
    mock_uploader.upload_file.return_value = 'new_url'

    data = {'title': 'Updated', 'description': 'Updated Desc'}
    file = FileStorage(filename='new_image.jpg')

    with patch('backend.service.recipe_service.get_jwt_identity', return_value=user_id):
        result = recipe_service.update(recipe.id, data, file)

    assert result['title'] == 'Updated'
    mock_uploader.upload_file.assert_called_once()
    mock_repo.update.assert_called_once()


def test_delete_recipe_success(recipe_service, mock_repo, mock_uploader):
    user_id = uuid4()
    recipe = Recipe(title='ToDelete', description='Desc', duration=10, servings_count=1, author_id=user_id)
    recipe.id = uuid4()
    recipe.image_url = 'image.jpg'
    mock_repo.get_by_id.return_value = recipe

    with patch('backend.service.recipe_service.get_jwt_identity', return_value=user_id), \
         patch('backend.service.recipe_service.get_jwt', return_value={'role': 'User'}):
        result = recipe_service.delete(recipe.id)

    assert result is True
    mock_uploader.delete_file.assert_called_once_with('image.jpg')
    mock_repo.delete.assert_called_once_with(recipe)
