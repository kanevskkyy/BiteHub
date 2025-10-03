from uuid import uuid4

import pytest
from werkzeug.datastructures import FileStorage
from flask_restx import ValidationError as FlaskRestxValidationError

from backend.exceptions import NotFound, AlreadyExists, ValidationError
from backend.models import Ingredient
from backend.schemas import ingredient_schema


def test_get_all_ingredients(ingredients_service, mock_repo):
    ing1 = Ingredient(name='ing1', icon_url='icon1.jpg')
    ing2 = Ingredient(name='ing2', icon_url='icon2.jpg')
    mock_repo.get_all.return_value = [ing1, ing2]

    result = ingredients_service.get_all()

    assert len(result) == 2
    assert result[0]['name'] == 'ing1'
    assert result[1]['iconUrl'] == 'icon2.jpg'
    mock_repo.get_all.assert_called_once()


def test_get_by_id_found(ingredients_service, mock_repo):
    ing = Ingredient(name='ing', icon_url='icon.jpg')
    ing.id = uuid4()
    mock_repo.get_by_id.return_value = ing

    result = ingredients_service.get_by_id(ing.id)
    assert result['name'] == 'ing'
    assert result['iconUrl'] == 'icon.jpg'
    mock_repo.get_by_id.assert_called_once_with(ing.id)


def test_get_by_id_not_found(ingredients_service, mock_repo):
    mock_repo.get_by_id.return_value = None
    ing_id = uuid4()

    with pytest.raises(NotFound):
        ingredients_service.get_by_id(ing_id)


def test_create_ingredient_success(ingredients_service, mock_repo, mock_uploader):
    data = {'name': 'new_ing'}
    file = FileStorage(filename='icon.jpg')
    mock_repo.is_name_exists.return_value = False
    mock_uploader.upload_file.return_value = 'uploaded_url'

    created_ing = Ingredient(name='new_ing', icon_url='uploaded_url')
    created_ing.id = uuid4()
    mock_repo.create.return_value = created_ing

    result = ingredients_service.create(data, icon_file=file)
    assert result['iconUrl'] == 'uploaded_url'
    mock_repo.is_name_exists.assert_called_once_with('new_ing')
    mock_repo.create.assert_called_once()
    mock_uploader.upload_file.assert_called_once_with(file, folder='ingredients')


def test_create_ingredient_already_exists(ingredients_service, mock_repo):
    data = {'name': 'exists'}
    mock_repo.is_name_exists.return_value = True
    with pytest.raises(AlreadyExists):
        ingredients_service.create(data, icon_file=FileStorage(filename='icon.jpg'))


def test_create_ingredient_no_file(ingredients_service, mock_repo):
    data = {'name': 'new_ing'}
    mock_repo.is_name_exists.return_value = False
    with pytest.raises(ValidationError):
        ingredients_service.create(data, icon_file=None)


def test_update_ingredient_success(ingredients_service, mock_repo, mock_uploader):
    ing = Ingredient(name='old', icon_url='old.jpg')
    ing.id = uuid4()
    mock_repo.get_by_id.return_value = ing
    mock_repo.is_name_exists.return_value = False
    mock_uploader.upload_file.return_value = 'new_icon.jpg'
    mock_repo.update.return_value = ing

    data = {'name': 'updated'}
    file = FileStorage(filename='icon.jpg')
    result = ingredients_service.update(ing.id, data, icon_file=file)

    assert result['name'] == 'updated'
    assert result['iconUrl'] == 'new_icon.jpg'
    mock_repo.get_by_id.assert_called_once_with(ing.id)
    mock_repo.update.assert_called_once()
    mock_uploader.upload_file.assert_called_once_with(file, folder='ingredients')


def test_update_ingredient_not_found(ingredients_service, mock_repo):
    mock_repo.get_by_id.return_value = None
    ing_id = uuid4()
    with pytest.raises(NotFound):
        ingredients_service.update(ing_id, {'name': 'updated'})


def test_update_ingredient_already_exists(ingredients_service, mock_repo):
    ing = Ingredient(name='old', icon_url='old.jpg')
    ing.id = uuid4()
    mock_repo.get_by_id.return_value = ing
    mock_repo.is_name_exists.return_value = True

    with pytest.raises(AlreadyExists):
        ingredients_service.update(ing.id, {'name': 'duplicate'})


def test_delete_ingredient_success(ingredients_service, mock_repo, mock_uploader):
    ing = Ingredient(name='del', icon_url='icon.jpg')
    ing.id = uuid4()
    mock_repo.get_by_id.return_value = ing

    result = ingredients_service.delete(ing.id)
    assert result is True
    mock_uploader.delete_file.assert_called_once_with('icon.jpg')
    mock_repo.delete.assert_called_once_with(ing)


def test_delete_ingredient_not_found(ingredients_service, mock_repo):
    mock_repo.get_by_id.return_value = None
    ing_id = uuid4()
    with pytest.raises(NotFound):
        ingredients_service.delete(ing_id)


def test_ingredient_schema_name_empty():
    data = {'name': '', 'iconUrl': 'icon.jpg'}
    with pytest.raises(FlaskRestxValidationError):
        ingredient_schema.load(data)

def test_ingredient_schema_name_too_long():
    data = {'name': 'a' * 101, 'iconUrl': 'icon.jpg'}
    with pytest.raises(FlaskRestxValidationError):
        ingredient_schema.load(data)