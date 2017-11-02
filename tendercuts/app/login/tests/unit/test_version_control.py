"""Test customer mobile version."""
import pytest
from app.login.lib.mobile_version_controller import MobileVersionControl


@pytest.mark.django_db
class TestVersionControl:
    """Test cases for customer mobile control version."""

    @pytest.mark.parametrize("mob_ver, status",
                             [('1.9.1', {"upgraded": False,
                                         "mandatory_upgrade": True}),
                              ('1.9.5', {"upgraded": True,
                                         "mandatory_upgrade": False})])
    def test_version_control(self, mob_ver, status):
        """Test Customer mobile version.

        Asserts:
            Check version

        """
        version = MobileVersionControl()
        status1 = version.version_comparision(mob_ver)

        assert status1['upgraded'] == status['upgraded']

        assert status1['mandatory_upgrade'] == status["mandatory_upgrade"]
