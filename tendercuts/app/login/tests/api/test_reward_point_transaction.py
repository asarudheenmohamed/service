import pytest

class TestReward:
    def test_rewardtransection(self,db,auth_rest):
        response = auth_rest.get(
            "/user/reward/",
            format='json')
        assert type(response) is not None
        assert response.status_code == 200
        assert response.json()[0]['customer']==18963

