from unittest.mock import patch
from uuid import uuid4

import pytest

from backend.exceptions import AlreadyExists
from backend.models import Reviews


@patch('backend.service.review_service.get_jwt_identity')
@patch('backend.service.review_service.get_jwt')
def test_delete_review_as_admin(mock_get_jwt, mock_get_jwt_identity, review_service, mock_repo):
    user_id = uuid4()
    review = Reviews()
    review.user_id = uuid4()
    review.id = uuid4()

    mock_repo.get_by_id.return_value = review
    mock_get_jwt_identity.return_value = user_id
    mock_get_jwt.return_value = {'role': 'Admin'}

    result = review_service.delete_review(review.id)
    assert result is True
    mock_repo.delete.assert_called_once_with(review)


@patch('backend.service.review_service.get_jwt_identity')
def test_create_review_already_exists(mock_get_jwt_identity, review_service, mock_repo):
    mock_get_jwt_identity.return_value = uuid4()
    mock_repo.is_user_already_rated.return_value = True

    with pytest.raises(AlreadyExists):
        review_service.create_review({'recipe_id': uuid4(), 'rating': 5, 'comment': 'Good!'})


@patch('backend.service.review_service.get_jwt_identity')
def test_create_review_success(mock_get_jwt_identity, review_service, mock_repo):
    user_id = uuid4()
    mock_get_jwt_identity.return_value = user_id
    mock_repo.is_user_already_rated.return_value = False
    mock_repo.get_pending_status_id.return_value = uuid4()

    review_instance = Reviews()
    mock_repo.create.return_value = review_instance

    result = review_service.create_review({'recipe_id': uuid4(), 'rating': 5, 'comment': 'Nice'})
    assert result is not None
    mock_repo.create.assert_called_once()