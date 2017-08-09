import os

import pytest
import pandas as pd


@pytest.fixture
def mock_df():
    """Mock Excel file."""
    path = os.path.join(os.path.dirname(__file__), "test.xlsx")
    inventory = pd.read_excel(path, skiprows=[0, 1, 2, 3])

    return inventory


@pytest.fixture
def file_path():
    """File path of the test excel."""
    return os.path.join(os.path.dirname(__file__), "test.xlsx")
