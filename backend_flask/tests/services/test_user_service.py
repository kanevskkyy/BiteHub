from datetime import datetime, timezone
from uuid import uuid4
from unittest.mock import Mock, patch
from werkzeug.datastructures import FileStorage


def test_get_by_id_found(user_service, mock_repo):
    user_id = uuid4()
    mock_user = Mock()
    mock_user.id = user_id
    mock_user.username = 'testuser'
    mock_user.description = 'desc'
    mock_user.first_name = 'John'
    mock_user.last_name = 'Doe'
    mock_user.avatar_url = 'url'
    mock_user.created_at = datetime.now(timezone.utc)

    mock_repo.get_by_id.return_value = mock_user

    result = user_service.get_by_id(user_id)

    assert result['id'] == str(user_id)
    assert result['username'] == 'testuser'
    mock_repo.get_by_id.assert_called_once_with(user_id)


def test_update_user_success(user_service, mock_repo, mock_uploader):
    user_id = uuid4()
    mock_user = Mock()
    mock_user.id = user_id
    mock_user.avatar_url = 'old_url'
    mock_user.created_at = datetime.now(timezone.utc)

    data = {
        'username': 'newuser',
        'description': 'newdesc',
        'first_name': 'John',
        'last_name': 'Doe'
    }

    mock_repo.get_by_id.return_value = mock_user
    mock_repo.is_username_exist.return_value = False
    mock_repo.update.return_value = mock_user
    mock_uploader.upload_file.return_value = 'new_url'

    with patch('backend.service.user_service.get_jwt_identity', return_value=user_id):
        result = user_service.update_user(user_id, data, FileStorage(filename='avatar.jpg'))

    assert result['username'] == 'newuser'
    mock_uploader.delete_file.assert_called_once_with('old_url')
    mock_uploader.upload_file.assert_called_once()
    mock_repo.update.assert_called_once()