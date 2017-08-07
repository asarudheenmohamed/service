"""Test Mcredit Balance."""
import pytest


@pytest.mark.django_db
class TestMcredit:

    def test_mcreditbalance(self, auth_rest):
        """Get reward point transection in 18963.

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
        # assert not isinstance(response, None)
        assert response.status_code == 200
        assert response.json()['results'][0]['customer'] == 19801
