"""Test Mcredit Balance."""
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
        assert type(response) is not None
        assert response.status_code == 200
        assert response.json()[0]['customer'] == 18963