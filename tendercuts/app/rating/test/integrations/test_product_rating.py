"""Integration tests for Product review and rating feature."""

import pytest
from pytest_bdd import given, scenario, then, when
from app.core.models import SalesFlatOrder
from app.rating.models import Rating, RatingTag


@pytest.mark.django_db
@scenario(
    'product_rating.feature',
    'Customer review and rating for a product purchased',
)
def test_product_rating():
    pass


@given('A customer placed an order')
def create_order(cache, generate_mock_order):
    """A customer create an order"""
    cache['increment_id'] = generate_mock_order.increment_id


@given("Add a rating Tag creation")
def create_rating_tag():
    """Create Rating Tags"""
    RatingTag.objects.create(tag_name='Delivery', threshold=3)
    RatingTag.objects.create(tag_name='Quality', threshold=2)
    RatingTag.objects.create(tag_name='Packing', threshold=3)


@given('Fetch all rating Tags')
def fetch_all_rating_tags(cache, auth_rest):
    """Fetch all rating tags.

    params:
        auth_rest (fixture) - user auth object.

    """
    rating_tags = auth_rest.get(
        "/rating/rating_tags/", format='json')
    rating_tag_ids = []
    for rating_tag in rating_tags.data['results']:
        rating_tag_ids.append(rating_tag['id'])
    cache['rating_tag_ids'] = rating_tag_ids


@given('A customer shares feedback for the product purchased on rating <comments><rating>')
def customer_create_a_rating(cache, auth_rest, comments, rating):
    """Assign the order.

    params:
        comments (str): Customer review.
        rating (str): customer rating
        auth_rest (fixture): user auth object.

    """
    response = auth_rest.post(
        "/rating/rating_create/",
        {'increment_id': cache['increment_id'],
         'rating': rating,
         'comments': comments,
         'rating_tag': cache['rating_tag_ids'],
         },
        format='json')

    assert (response) is not None
    assert response.status_code == 201
    assert response.data['status'] == True


@then('Cross check review rating <comments>')
def checks_the_customer_rating(cache, auth_rest, comments):
    """Assign the order.

    params:
        comments (str): Customer review.
        auth_rest (fixture): user auth object.
    """
    rating_obj = Rating.objects.filter(
        increment_id=cache['increment_id']).last()

    assert rating_obj.rating == 2
    assert rating_obj.comments == comments
