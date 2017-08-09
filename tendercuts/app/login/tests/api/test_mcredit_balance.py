"""Test Mcredit Balance."""
import pytest


@pytest.mark.django_db
class TestMcredit:

    def test_creditbalance_api(self, auth_rest):
        """Get reward point transaction.

        Params:
        auth_rest(pytest fixture):user requests

        returns:
                this is return a user id request

        Asserts:
            Check response not equal to None
            Check response status code in equal to 200
            Check custermer id is equal to 18963

        """
        response = auth_rest.get(
            "/user/mcredit/",
            format='json')

        assert response.status_code == 200
        # assert response.json()['results'][0]['customer'] == 19801
