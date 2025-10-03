import pytest
from uuid import uuid4
from unittest.mock import Mock, patch
from werkzeug.datastructures import FileStorage
from backend.exceptions import AlreadyExists, NotFound, ValidationError


def test_check_username_exist_true(auth_service, mock_user_repo):
    mock_user_repo.is_username_exist.return_value = True
    result = auth_service.check_username_exist('existing_user')
    assert result['exists'] is True
    mock_user_repo.is_username_exist.assert_called_once_with('existing_user')


def test_check_username_exist_false(auth_service, mock_user_repo):
    mock_user_repo.is_username_exist.return_value = False
    result = auth_service.check_username_exist('new_user')
    assert result['exists'] is False
    mock_user_repo.is_username_exist.assert_called_once_with('new_user')


def test_register_user_success(auth_service, mock_user_repo, mock_role_repo, mock_uploader):
    user_id = uuid4()
    data = {
        'username': 'newuser',
        'password_hash': 'Password1',
        'first_name': 'John',
        'last_name': 'Doe',
        'description': 'desc',
        'confirm_password': 'Password1'
    }
    mock_user_repo.is_username_exist.return_value = False

    role = Mock()
    role.id = uuid4()
    role.name = 'User'
    mock_role_repo.get_role_by_name.return_value = role

    mock_user = Mock()
    mock_user.id = user_id
    mock_user.role = role
    mock_user_repo.create.return_value = mock_user
    mock_uploader.upload_file.return_value = 'uploaded_url'

    with patch('backend.service.auth_service.create_access_token', return_value='access123'), \
         patch('backend.service.auth_service.create_refresh_token', return_value='refresh123'):
        result = auth_service.register_user(data, FileStorage(filename='avatar.jpg'))

    assert result['accessToken'] == 'access123'
    assert result['refreshToken'] == 'refresh123'
    mock_user_repo.create.assert_called_once()
    mock_uploader.upload_file.assert_called_once()


def test_register_user_username_exists(auth_service, mock_user_repo):
    mock_user_repo.is_username_exist.return_value = True
    data = {'username': 'existing', 'password_hash': 'Password1'}
    with pytest.raises(AlreadyExists):
        auth_service.register_user(data)


def test_login_user_success(auth_service, mock_user_repo):
    user_id = uuid4()
    mock_user = Mock()
    mock_user.id = user_id
    mock_user.role.name = 'User'
    mock_user.check_password.return_value = True
    mock_user_repo.get_user_by_username.return_value = mock_user

    data = {'username': 'user1', 'password': 'Password1'}
    with patch('backend.service.auth_service.create_access_token', return_value='access123'), \
         patch('backend.service.auth_service.create_refresh_token', return_value='refresh123'):
        result = auth_service.login_user(data)

    assert result['accessToken'] == 'access123'
    assert result['refreshToken'] == 'refresh123'


def test_login_user_invalid(auth_service, mock_user_repo):
    mock_user_repo.get_user_by_username.return_value = None
    data = {'username': 'user1', 'password': 'Password1'}
    with pytest.raises(ValidationError):
        auth_service.login_user(data)


def test_refresh_access_token_success(auth_service, mock_user_repo):
    user_id = uuid4()
    mock_user = Mock()
    mock_user.id = user_id
    mock_user.role.name = 'User'
    mock_user_repo.get_by_id.return_value = mock_user

    with patch('backend.service.auth_service.get_jwt_identity', return_value=user_id), \
         patch('backend.service.auth_service.create_access_token', return_value='new_access'):
        token = auth_service.refresh_access_token()

    assert token == 'new_access'


def test_refresh_access_token_not_found(auth_service, mock_user_repo):
    mock_user_repo.get_by_id.return_value = None
    with patch('backend.service.auth_service.get_jwt_identity', return_value=uuid4()):
        with pytest.raises(NotFound):
            auth_service.refresh_access_token()


def test_change_password_success(auth_service, mock_user_repo):
    user_id = uuid4()
    mock_user = Mock()
    mock_user.id = user_id
    mock_user.check_password.side_effect = [True, False]
    mock_user_repo.get_by_id.return_value = mock_user

    data = {'old_password': 'old', 'new_password': 'new'}

    with patch('backend.service.auth_service.get_jwt_identity', return_value=user_id):
        result = auth_service.change_password(data)

    assert result is True
    mock_user.set_password.assert_called_once_with('new')
    mock_user_repo.update.assert_called_once()


def test_change_password_wrong_old(auth_service, mock_user_repo):
    user_id = uuid4()
    mock_user = Mock()
    mock_user.id = user_id
    mock_user.check_password.return_value = False
    mock_user_repo.get_by_id.return_value = mock_user

    data = {'old_password': 'old', 'new_password': 'new'}

    with patch('backend.service.auth_service.get_jwt_identity', return_value=user_id):
        with pytest.raises(ValidationError):
            auth_service.change_password(data)


def test_change_password_same_as_old(auth_service, mock_user_repo):
    user_id = uuid4()
    mock_user = Mock()
    mock_user.id = user_id
    mock_user.check_password.side_effect = [True, True]
    mock_user_repo.get_by_id.return_value = mock_user

    data = {'old_password': 'old', 'new_password': 'old'}

    with patch('backend.service.auth_service.get_jwt_identity', return_value=user_id):
        with pytest.raises(ValidationError):
            auth_service.change_password(data)
