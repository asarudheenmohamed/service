import pytest

@pytest.fixture(scope="session")
def test_user():
    return 18963