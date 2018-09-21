"""Integration tests for notify inventory module."""
import datetime

import pytest
from pytest_bdd import given, scenario, then, when

from app.core.models import Graminventory
from app.inventory.lib import InventoryRequestController
from app.inventory.models import InventoryRequest, Inventorylog
from app.inventory.serializers import InventoryRequestSerializer


@pytest.mark.django_db
@scenario(
    'flock_update.feature',
    'The request is approved by controller w/w/o initial inventory'
)
def test_flock_approval_flow():
    """Check the inventory flow."""
    pass


@pytest.mark.django_db
@scenario(
    'flock_update.feature',
    'The request is rejected by controller'
)
def test_flock_reject_flow():
    """Check the inventory flow."""
    pass


@pytest.mark.django_db
@scenario(
    'flock_update.feature',
    'The request is auto approved'
)
def test_auto_approve_flow():
    """Check the inventory flow."""
    pass


def mock_inv(product):
    try:
        entry = Graminventory.objects.get(
            store_id=1, product_id=product, date=datetime.date.today())
        entry.delete()
    except:
        pass

    return Graminventory.objects.create(
        date=datetime.date.today(),
        product_id=product,
        store_id=1,
        opening=0,
        qty=100,
        expiringtoday=0,
        forecastqty=100
    )


@pytest.fixture(autouse=True)
def cleanup():
    """Nuke all records before starting"""
    Inventorylog.objects.all().delete()
    Graminventory.objects.all().delete()


@given('setup initial inventory for <product1> and <product2> if flag <is_initial_set>')
def initial_inventory(product1, product2, is_initial_set):
    """Set up the initial inventory if the is_initial_set flag is set to true."""
    if not is_initial_set:
        return

    for data in [product1, product2]:
        product_id, sku, qty = data.split(',')
        mock_inv(product_id)


@given('create <type> request for <product1> and <product2>')
def create_request(mock_sm, auth_sm, type, product1, product2, cache):
    """Create mock requests and trigger api calll"""
    request_type = InventoryRequest.INV_TYPE.TODAY.value if type == 'today' \
        else InventoryRequest.INV_TYPE.TOMO.value

    datum = []
    for data in [product1, product2]:
        product_id, sku, qty = data.split(',')
        datum.append({
            'product_id': product_id,
            'sku': sku,
            'product_name': 'foor',
            'store_id': 1,
            'store_name': 'thp',
            'type': request_type,
            'gpu': 550,
            'qty': qty,
            'triggered_by': mock_sm.id
        })

    response = auth_sm.post(
        "/store_manager/inv_request/",
        datum,
        format='json')

    assert response.status_code == 201, response.json()

    cache['ids'] = [record['id'] for record in response.json()]


@when('the inventory requests are approved')
def approve_request(cache, auth_im):
    """Mock the im approvals"""
    requests = InventoryRequest.objects.filter(id__in=cache['ids'])
    data = InventoryRequestSerializer(requests, many=True)

    for record in data.data:
        record['status'] = 1

        response = auth_im.put(
            "/store_manager/pending_inv_request/{}/".format(record['id']),
            dict(record),
            format='json')

        assert response.status_code == 200, response.json()
        request = InventoryRequest.objects.get(pk=record['id'])
        assert request.status == InventoryRequest.Status.APPROVED.value


@when('the inventory requests are auto approved')
def auto_approve(cache):
    """Mock the cron approvals"""
    InventoryRequestController.auto_approve_expired_request(test_mode=True)
    requests = InventoryRequest.objects.filter(id__in=cache['ids'])

    for record in requests:
        assert record.status == InventoryRequest.Status.APPROVED.value


@when('the inventory requests are rejected')
def reject_requests(cache, auth_im):
    """Mock the reject approvals"""
    requests = InventoryRequest.objects.filter(id__in=cache['ids'])
    data = InventoryRequestSerializer(requests, many=True)

    for record in data.data:
        record['status'] = 2

        response = auth_im.put(
            "/store_manager/pending_inv_request/{}/".format(record['id']),
            dict(record),
            format='json')

        assert response.status_code == 200, response.json()
        request = InventoryRequest.objects.get(pk=record['id'])
        assert request.status == InventoryRequest.Status.REJECTED.value


@then('inventory <type> should have logs with <qty1> and <qty2> with <is_initial_set>')
def verify_logs(cache, type, qty1, qty2, is_initial_set):
    """Asserts:
        Verify if logs are set
    """
    requests = InventoryRequest.objects.filter(id__in=cache['ids'])

    # Used in log tables
    type_of_qty = 'qty' if type == "today" else 'forecastqty'

    qty = dict([qty1.split(','), qty2.split(',')])

    for record in requests:  # type: InventoryRequest

        expected_qty = qty[str(record.product_id)]
        log = Inventorylog.objects.get(
            sku=record.sku,
            store_id=record.store_id,
            type_of_qty=type_of_qty,
            createdat__gt=record.created_time.date()
        )

        if is_initial_set:
            assert float(log.stockupdatedfrom) == float(100)
        assert float(log.stockupdatedto) == float(expected_qty)
        assert len(log.message) > 0


@then('inventory <type> should become live with <qty1> and <qty2>')
def verify_inventory(cache, type, qty1, qty2):
    """
    Asserts
        - If the qty is correct
        - log message is added
        - approved by is set
        - request is approved
    """
    requests = InventoryRequest.objects.filter(id__in=cache['ids'])

    # Used in log tables
    type_of_qty = 'qty' if type == "today" else 'forecastqty'

    # Used in inv request tables
    request_type = InventoryRequest.INV_TYPE.TODAY.value if type == 'today' \
        else InventoryRequest.INV_TYPE.TOMO.value
    qty = dict([qty1.split(','), qty2.split(',')])

    for record in requests:  # type: InventoryRequest
        new_inv = Graminventory.objects.get(
            date=record.created_time.date(),
            store_id=record.store_id,
            product_id=record.product_id
        )  # type: Graminventory

        expected_qty = qty[str(record.product_id)]

        # check if qty/forecastqty is udpated
        assert float(getattr(new_inv, type_of_qty)) == float(expected_qty)

        assert record.type == request_type


@then('verify user approved is set')
def verify_inventory(cache, mock_im):
    """
    Asserts
        - approved by is set
    """
    requests = InventoryRequest.objects.filter(id__in=cache['ids'])

    for record in requests:  # type: InventoryRequest
        assert record.approved_by_id == mock_im.id
