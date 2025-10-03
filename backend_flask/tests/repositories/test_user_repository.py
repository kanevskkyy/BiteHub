from backend.models import User, Role
from backend.repositories import UserRepository, RoleRepository
from tests.conftest import db_session


def test_create_user(db_session):
    user_repo = UserRepository()
    role_repo = RoleRepository()

    role = Role(name='User')
    role = role_repo.create(role)

    user = User(
        username='testuser',
        first_name='Test',
        last_name='User',
        role_id=role.id,
    )
    user.set_password('password123')

    created_user = user_repo.create(user)

    assert created_user.id is not None
    assert created_user.username == 'testuser'
    assert created_user.check_password('password123')
    assert not created_user.check_password('wrongpassword')


def test_is_username_exist(db_session):
    repo = UserRepository()
    role_repo = RoleRepository()

    role = Role(name='User')
    role = role_repo.create(role)

    user = User(
        username='existinguser',
        first_name='Exist',
        last_name='User',
        role_id=role.id,
    )
    user.set_password('password123')
    repo.create(user)

    assert repo.is_username_exist('existinguser') is True
    assert repo.is_username_exist('notexist') is False

    assert repo.is_username_exist('existinguser', exclude_id=user.id) is False


def test_get_user_by_username(db_session):
    repo = UserRepository()
    role_repo = RoleRepository()

    role = Role(name='User')
    role = role_repo.create(role)

    user = User(
        username='findme',
        first_name='Find',
        last_name='Me',
        role_id=role.id,
    )
    user.set_password('secret')
    repo.create(user)

    found = repo.get_user_by_username('findme')
    assert found is not None
    assert found.username == 'findme'
    assert found.check_password('secret')

    assert repo.get_user_by_username('doesnotexist') is None


def test_update_user(db_session):
    user_repo = UserRepository()
    role_repo = RoleRepository()

    role = Role(name='User')
    role = role_repo.create(role)

    user = User(
        username='findme',
        first_name='Find',
        last_name='Me',
        role_id=role.id,
    )
    user.set_password('secret')
    user = user_repo.create(user)

    assert user.username == 'findme'

    user.username = 'new_cool_username'
    user_repo.update(user)

    assert user_repo.get_by_id(user.id).username == 'new_cool_username'