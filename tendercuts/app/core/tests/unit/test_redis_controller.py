"""End Point for the test redis controller."""
import pytest

from app.core.lib.otp_controller import OtpController
from app.core.lib.redis_controller import RedisController


@pytest.mark.django_db
class TestRdisController:
    """Test redis controller."""

    def test_redis_save(self):
        """Test redis controller save method.

        Asserts:
          Check redis status is equal to True

        """
        redis_obj = RedisController()
        otp = OtpController().create_otp(9908765678)
        obj = redis_obj.redis_save(otp, 'FORGOT')
        assert obj == True

    def test_redis_set(self):
        """Test redis controller set method.

        Asserts:
          Check redis status is equal to True

        """
        redis_obj = RedisController()
        obj = redis_obj.set(9908765678, 'verified')
        assert obj == True

    def test_redis_get(self):
        """Test redis controller get method.

        Asserts:
          Check object mobile number is equal to True

        """
        redis_obj = RedisController()
        obj = redis_obj.redis_get(9908765678, 'FORGOT')
        assert obj.mobile == 9908765678

    def test_get(self):
        """Test redis controller get method.

        Asserts:
          Check object mobile number is equal to True

        """
        redis_obj = RedisController()
        val = redis_obj.get(9908765678)
        assert val == 'verified'
