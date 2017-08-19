"""
Test cases for inventory upload controller.
"""

import pandas as pd
import pytest

from app.inventory.lib import InventoryUploadController
from app.core.models import AitocCataloginventoryStockItem


@pytest.fixture
def controller(mock_df):
    """Fixture.

    params:
        dummy_file(fixture): Fixture for mock file.

    Generate an class instance
    """
    return InventoryUploadController(mock_df)


@pytest.mark.django_db
class TestInventoryUploadController(object):
    """Test cases for Inventory upload controller."""

    def test_inv_upload_cleanup(self, controller):
        """File upload test.

        Params:
            1. controller (fixture) instance

        Asserts:
            1. The df is cleaned properly
        """
        expected = [
            u'adayar', u'thoraipakkam', u'porur', u'tambaram', u'arumbakkam',
            u'tpos', u'adayar.1', u'thoraipakkam.1', u'porur.1', u'tambaram.1',
            u'arumbakkam.1', u'tpos.1', u'Total Qty']
        controller.cleanup()
        assert controller.inventory.columns.tolist() == expected

    def test_inv_update(self, controller):
        """Check for the value un DB.

        Params:
            1. Controller (fixture) : instance

        Asserts:
            1. If the DB has been updated.
        """
        controller.process()

        products = AitocCataloginventoryStockItem.objects \
            .all().filter(product_id=192)

        expected = {
            1: 98,  # tpakkam
            2: 103,  # adyar,
            3: 97,  # porur
            4: 97,  # Tambar
            5: 101  # Arum
        }

        for product in products:
            if product.website_id in expected.keys():
                assert expected[product.website_id] == product.qty
