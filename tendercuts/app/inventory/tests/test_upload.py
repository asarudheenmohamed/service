"""
Test cases for inventory upload endpoint
"""
import requests_toolbelt
import StringIO
import os


class TestInventoryUpload(object):
    """Test cases for Inventory upload.

    1. Inventory upload.
    """

    def test_inventory_upload(self, auth_rest):
        """File upload test.

        Assserts:
            1. If invetory file is obtained
            2. the inventory value changes in DB for that store.
        """
        path = os.path.join(os.path.dirname(__file__), "test.xlsx")
        response = auth_rest.post(
            "/inventory/upload/test.xlsx",
            data={'file': open(path, 'rb')},
            format='multipart')

        assert response.status_code == 204
