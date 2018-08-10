"""Test cases for Cms Endpoints."""

import pytest
from app.core.models.cms import CmsPage


@pytest.mark.django_db
class TestCms(object):
    """Test cases for cms related api's."""

    def test_cms_api(self, rest):
        """Test to the cms viewset api..

        params:
            rest (fixture): rest endpoint

        Asserts:
            Checks the response status code
            Checks the response is not None

        """
        response = rest.get("/core/get_cms_footer/", format='json')

        assert (response) is not None
        assert response.status_code == 200
        assert len(response.data) != 0

        response = rest.get(
            "/core/cms/?title={}".format(response.data[0]['title']), format='json')

        assert (response) is not None
        assert response.status_code == 200
        assert len(response.data) != 0
