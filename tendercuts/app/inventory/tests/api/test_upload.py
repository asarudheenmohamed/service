"""Test cases for inventory upload endpoint."""

import os
import pytest


@pytest.mark.django_db
class TestInventoryUpload(object):
    """Test cases for Inventory upload.

    1. Inventory upload.
    """

    def test_inventory_upload(self, auth_rest, file_path):
        """File upload test.

        Assserts:
            1. If invetory file is obtained
            2. the inventory value changes in DB for that store.
        """
        response = auth_rest.post(
            "/inventory/upload/test.xlsx",
            data={'file': open(file_path, 'rb')},
            format='multipart')

        assert response.status_code == 204
