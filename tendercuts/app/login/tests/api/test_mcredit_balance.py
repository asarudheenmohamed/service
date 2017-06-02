import pytest


class TestMcredit:
    def test_mcreditbalance(self, db, auth_rest):
        response = auth_rest.get(
            "/user/mcredit/",
            format='json')
        assert type(response) is not None
        assert response.status_code == 200
        assert response.json()[0]['customer'] == 18963