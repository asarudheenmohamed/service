import pytest

@pytest.mark.django_db
def test_create_delete_payment_mode(auth_rest):
    """Fetch API modes.

    Asserts:
        1. Get request fetches NB and card details from JP

    """
    data = {
        'title': "4242424242424242",
        'pin' : "111",
        'expiry_year' : "2020",
        'expiry_month': "10",
        'method': "juspay",
        'gateway_code': "CARD"
    }
    response = auth_rest.post("/payment/payment_mode/", data=data)
    assert response.status_code == 201
    response = auth_rest.delete("/payment/payment_mode/delete/", data=data)
    print (response.__dict__)
    assert response.status_code == 204
