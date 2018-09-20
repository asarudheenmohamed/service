import pytest

data = [
    {
        "product_id": 200,
        "store_id": 1,
        "qty": 1,
        "store_name": "thoraipakkam",
        "product_name": "Minced Chicken",
        "sku": "CHK_MINCE ",
        "type": 0,
        "gpu": "550"
    },
    {
        "product_id": 193,
        "store_id": 1,
        "qty": 2,
        "store_name": "thoraipakkam",
        "product_name": "Chicken Curry Cut (Skin Off)",
        "sku": "CHK_WHL_SKIN_OFF ",
        "type": 0,
        "gpu": "525"
    },
    {
        "product_id": 199,
        "store_id": 1,
        "qty": 3,
        "store_name": "thoraipakkam",
        "product_name": "Chicken Breast Boneless",
        "sku": "CHK_BR_BONELESS ",
        "type": 0,
        "gpu": "300"
    }
]


@pytest.mark.django_db
def test_verify_create_requests(auth_sm):
    response = auth_sm.post(
        "/store_manager/inv_request/",
        data,
        format='json',
    )

