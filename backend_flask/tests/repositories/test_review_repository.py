from backend.models import Reviews, ReviewStatus, User, Recipe
from backend.repositories import ReviewRepository, RoleRepository, UserRepository

def test_review_repository_methods(db_session):
    role_repo = RoleRepository()
    role = role_repo.create(role_repo._model(name='TestRole'))

    user_repo = UserRepository()
    user = User(username='test_user', first_name='Test', last_name='User', role_id=role.id)
    user.set_password('password123')
    user = user_repo.create(user)

    recipe = Recipe(title='Test Recipe', description='Desc', duration=30, author_id=user.id, servings_count=2)
    db_session.add(recipe)
    db_session.commit()

    pending_status = ReviewStatus(name='pending')
    approved_status = ReviewStatus(name='approved')
    db_session.add_all([pending_status, approved_status])
    db_session.commit()

    repo = ReviewRepository()

    review = Reviews(user_id=user.id, recipe_id=recipe.id, status_id=pending_status.id, rating=5, comment='Nice')
    review = repo.create(review)

    assert repo.is_user_already_rated(user.id, recipe.id) is True
    assert repo.has_any_review(user.id, recipe.id) is True
    assert repo.has_approved_review(user.id, recipe.id) is False

    review.status_id = approved_status.id
    repo.update(review)
    assert repo.has_approved_review(user.id, recipe.id) is True

    paginated = repo.get_reviews_by_recipe(recipe.id, page=1, per_page=10)
    assert paginated.total == 1
    assert paginated.items[0].id == review.id

    paginated_pending = repo.get_pending_reviews(page=1, per_page=10)
    assert paginated_pending.total == 0

    assert repo.get_pending_status_id() == pending_status.id
    assert repo.get_approve_status_id() == approved_status.id


    repo.delete(review)
    assert repo.has_any_review(user.id, recipe.id) is False