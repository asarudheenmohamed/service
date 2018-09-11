"""Test cases for Ratingcontroller."""

import time

import pytest
from django.contrib.auth.models import User

from app.core.lib.communication import FreshDesk
from app.rating.lib.rating_controller import RatingController
from app.rating.models import Rating, RatingTag


@pytest.mark.django_db
class TestRatingController:
    """Test cases"""

    def test_create_fresh_desk_ticket(self, mock_user, generate_mock_order):
        """Test the fresh desk ticket creation.

        Params:
            mock_user (fix): mock user
            generate_mock_order(obj): order object

        Asserts:
            Check whether the response status.
        """

        tag_obj = RatingTag.objects.create(tag_name='delivery', threshold=3)
        user_obj = User.objects.get_or_create(
            username=mock_user.dj_user_id)[0]

        rating = Rating.objects.create(
            user=user_obj,
            comments='product is bad',
            rating=2)
        rating.rating_tag.add(tag_obj)
        rating.save()

        responce = RatingController(
            generate_mock_order.increment_id).create_fresh_desk_ticket()

        assert response.status_code == 200

        response = FreshDesk().delete_fresh_desk_ticket(responce['id'])

        assert response.status_code == 204
