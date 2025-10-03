from uuid import uuid4

import pytest
from werkzeug.datastructures import FileStorage

from backend.exceptions import NotFound, AlreadyExists, ValidationError
from backend.models import Category


def test_get_all_categories(category_service, mock_repo):
    cat1 = Category(name='cat1', icon_url='icon1.jpg')
    cat2 = Category(name='cat2', icon_url='icon2.jpg')
    mock_repo.get_all.return_value = [cat1, cat2]

    result = category_service.get_all()

    assert len(result) == 2
    assert result[0]['name'] == 'cat1'
    assert result[1]['iconUrl'] == 'icon2.jpg'
    mock_repo.get_all.assert_called_once()


def test_get_by_id_found(category_service, mock_repo):
    cat = Category(name='cat', icon_url='icon.jpg')
    cat.id = uuid4()
    mock_repo.get_by_id.return_value = cat

    result = category_service.get_by_id(cat.id)
    assert result['name'] == 'cat'
    mock_repo.get_by_id.assert_called_once_with(cat.id)


def test_get_by_id_not_found(category_service, mock_repo):
    mock_repo.get_by_id.return_value = None
    cat_id = uuid4()

    with pytest.raises(NotFound):
        category_service.get_by_id(cat_id)


def test_create_category_success(category_service, mock_repo, mock_uploader):
    data = {'name': 'new_cat'}
    file = FileStorage(filename='icon.jpg')
    mock_repo.is_name_exists.return_value = False
    mock_uploader.upload_file.return_value = 'uploaded_url'
    created_cat = Category(name='new_cat', icon_url='uploaded_url')
    mock_repo.create.return_value = created_cat

    result = category_service.create(data, icon_file=file)
    assert result['iconUrl'] == 'uploaded_url'
    mock_repo.is_name_exists.assert_called_once_with('new_cat')
    mock_repo.create.assert_called_once()
    mock_uploader.upload_file.assert_called_once_with(file, folder='category')


def test_create_category_already_exists(category_service, mock_repo):
    data = {'name': 'exists'}
    mock_repo.is_name_exists.return_value = True

    with pytest.raises(AlreadyExists):
        category_service.create(data, icon_file=FileStorage(filename='icon.jpg'))


def test_create_category_no_file(category_service, mock_repo):
    data = {'name': 'new_cat'}
    mock_repo.is_name_exists.return_value = False

    with pytest.raises(ValidationError):
        category_service.create(data, icon_file=None)


def test_update_category_success(category_service, mock_repo, mock_uploader):
    category = Category(name='old', icon_url='old.jpg')
    category.id = uuid4()
    mock_repo.get_by_id.return_value = category
    mock_repo.is_name_exists.return_value = False
    mock_uploader.upload_file.return_value = 'new_icon.jpg'
    mock_repo.update.return_value = category

    data = {'name': 'updated'}
    file = FileStorage(filename='icon.jpg')

    result = category_service.update(category.id, data, icon_file=file)
    assert result['name'] == 'updated'
    mock_repo.get_by_id.assert_called_once_with(category.id)
    mock_repo.update.assert_called_once()
    mock_uploader.upload_file.assert_called_once_with(file, folder='category')


def test_update_category_not_found(category_service, mock_repo):
    mock_repo.get_by_id.return_value = None
    cat_id = uuid4()

    with pytest.raises(NotFound):
        category_service.update(cat_id, {'name': 'updated'})


def test_update_category_already_exists(category_service, mock_repo):
    category = Category(name='old', icon_url='old.jpg')
    category.id = uuid4()
    mock_repo.get_by_id.return_value = category
    mock_repo.is_name_exists.return_value = True

    with pytest.raises(AlreadyExists):
        category_service.update(category.id, {'name': 'duplicate'})


def test_delete_category_success(category_service, mock_repo, mock_uploader):
    category = Category(name='del', icon_url='icon.jpg')
    category.id = uuid4()
    mock_repo.get_by_id.return_value = category

    result = category_service.delete(category.id)
    assert result is True
    mock_uploader.delete_file.assert_called_once_with('icon.jpg')
    mock_repo.delete.assert_called_once_with(category)


def test_delete_category_not_found(category_service, mock_repo):
    mock_repo.get_by_id.return_value = None
    cat_id = uuid4()

    with pytest.raises(NotFound):
        category_service.delete(cat_id)