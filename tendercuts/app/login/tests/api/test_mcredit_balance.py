"""Test Mcredit Balance."""
class TestMcredit:
    def test_mcreditbalance(self, auth_rest):
        """Get reard point transection in 18963.

        pytest fixture:auth_rest
            returns:
                this is return a user id request

        Tests:
            Check response not equal to None
            Check response status code in equal to 200
            Check custermer id is equal to 18963

        """
        response = auth_rest.get(
            "/user/mcredit/",
            format='json')
        assert type(response) is not None
        assert response.status_code == 200
        assert response.json()[0]['customer'] == 18963