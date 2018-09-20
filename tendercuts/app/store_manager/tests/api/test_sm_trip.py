import pytest


@pytest.mark.django_db
def test_verify_create_trip(auth_sm, mock_new_driver):
    response = auth_sm.post(
        "/store_manager/trips/",
        {'driver_user': mock_new_driver.id,
         'auto_assigned': True,
         'driver_order': ['1001', '1002']
         },
        format='json',
    )
    assert response.data['driver_user'] is not None
    assert response.data['auto_assigned'] is True
    assert len(response.data['driver_order']) > 0
    # assert len(response.json()['trip_created_time']) > 0
