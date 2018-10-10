import datetime

import pytest
from django.contrib.auth.models import User

from app.core.models import Graminventory
from app.inventory.lib import InventoryController
from app.inventory.models import InventoryRequest, Inventorylog


@pytest.fixture()
def mock_user():
    return User.objects.create_user(
        username="test", email="test@test.com",
        password='test')


@pytest.fixture()
def mock_inv():
    entry = Graminventory.objects.filter(
        store_id=1, product_id=193, date=datetime.date.today())
    if entry:
        entry.delete()
    except:
        pass

    return Graminventory.objects.create(
        date=datetime.date.today(),
        product_id=193,
        store_id=1,
        opening=0,
        qty=100,
        expiringtoday=0,
        forecastqty=100
    )


@pytest.mark.django_db()
def test_today_qty_upload(mock_inv, mock_user):
    """Assets if express works and there is a log"""
    req = InventoryRequest.objects.create(
        product_id=193,
        product_name='foor',
        store_id=1,
        type=0,
        qty=0,
        gpu=550,
        sku='CHK_SKU',
        store_name="THP",
        triggered_by=mock_user

    )

    log = InventoryController(mock_inv).process_inventory_request(req)

    new_inv = Graminventory.objects.get(
        pk=mock_inv.graminventoryid)  # type: Graminventory
    assert new_inv.qty == 0

    assert log.sku == req.sku
    assert log.stockupdatedfrom == 100
    assert log.stockupdatedto == 0
    assert log.store_id == req.store_id
    assert log.type_of_qty == 'qty'


@pytest.mark.django_db()
def test_tomo_qty_upload(mock_inv, mock_user):
    """Assets if shceduled works and there is a log"""
    req = InventoryRequest.objects.create(
        product_id=193,
        product_name='foor',
        store_id=1,
        type=1,
        qty=0,
        triggered_by=mock_user,
        gpu=1000
    )

    log = InventoryController(mock_inv).process_inventory_request(req)

    new_inv = Graminventory.objects.get(
        pk=mock_inv.graminventoryid)  # type: Graminventory
    assert new_inv.forecastqty == 0

    assert log.sku == req.sku
    assert log.stockupdatedfrom == 100
    assert log.stockupdatedto == 0
    assert log.store_id == req.store_id
    assert log.type_of_qty == 'forecastqty'
