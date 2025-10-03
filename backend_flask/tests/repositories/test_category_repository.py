from backend.models import Category
from backend.repositories import CategoryRepository


def test_create_category(db_session):
    repo = CategoryRepository()
    category = Category(name='test_category', icon_url='https://test.jpg')
    category = repo.create(category)

    found = repo.get_by_id(category.id)

    assert found is not None
    assert found.name == 'test_category'
    assert found.icon_url == 'https://test.jpg'


def test_get_all_categories(db_session):
    repo = CategoryRepository()

    categories = repo.get_all()
    assert categories == []

    category1 = Category(name='category_1', icon_url='https://test1.jpg')
    category2 = Category(name='category_2', icon_url='https://test2.jpg')
    repo.create(category1)
    repo.create(category2)

    categories = repo.get_all()

    assert categories is not None
    assert len(categories) == 2
    assert categories[0].name == 'category_1'
    assert categories[1].name == 'category_2'


def test_update_category(db_session):
    repo = CategoryRepository()
    category = Category(name='original_name', icon_url='https://test.jpg')
    category = repo.create(category)

    category_id = category.id

    category.name = 'updated_name'
    updated = repo.update(category)

    assert updated.id == category_id
    assert updated.name == 'updated_name'

    found = repo.get_by_id(category_id)
    assert found.name == 'updated_name'


def test_delete_category(db_session):
    repo = CategoryRepository()
    category = Category(name='to_be_deleted', icon_url='https://test.jpg')
    category = repo.create(category)

    category_id = category.id

    assert repo.get_by_id(category_id) is not None

    repo.delete(category)
    assert repo.get_by_id(category_id) is None


def test_is_name_exists(db_session):
    repo = CategoryRepository()

    category = Category(name='unique_name', icon_url='https://test.jpg')
    category = repo.create(category)

    assert repo.is_name_exists('unique_name') is True
    assert repo.is_name_exists('not_exist') is False

    assert repo.is_name_exists('unique_name', exclude_id=category.id) is False