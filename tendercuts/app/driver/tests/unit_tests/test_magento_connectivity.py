import app.tcuts.core.magento_api as mage
import pytest
import types

@pytest.fixture
def api():
    return mage.Connector().api


def test_connection(api):
    assert "help" in dir(api)





