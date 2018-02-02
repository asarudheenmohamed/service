"""Test customer mobile app version."""
import pytest
from django.conf import settings

from app.login.lib.app_version_controller import AppVersionControl


@pytest.mark.django_db
class TestVersionControl:
    """Test cases for customer app control version."""

    @pytest.mark.parametrize("mob_ver, status",
                             [('1.9.1', {"upgraded": False,
                                         "mandatory_upgrade": True}),
                              ('1.9.6', {"upgraded": True,
                                         "mandatory_upgrade": False})])
    def test_version_control(self, mob_ver, status):
        """Test Customer mobile app version.

        Asserts:
            Check version

        """
        MIN_VER = settings.APP_VERSIONS['CUSTOMER_APP_VERSION']['min_app_version']

        version = AppVersionControl()
        ctrl_status = version.version_comparision(mob_ver, MIN_VER)

        assert ctrl_status['upgraded'] == status['upgraded']

        assert ctrl_status['mandatory_upgrade'] == status["mandatory_upgrade"]
