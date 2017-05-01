import pytest
import app.core.models as models
import time


@pytest.fixture(scope="module")
def order_id(generate_mock_order):
    return generate_mock_order


@pytest.mark.django_db
@pytest.mark.incremental
class TestFetchOrder():
    @pytest.mark.django_db
    def test_mock_order_create(self, order_id):
        # move the order to out_delivery and assign a driver
        sales_order = models.SalesFlatOrder.objects.filter(increment_id=order_id)
        assert sales_order[0]

        sales_order = sales_order[0]
        sales_order.driver_id = 7
        sales_order.status = "out_delivery"
        # sales_order.status = "processing"
        sales_order.save()
        time.sleep(1)

    def test_fetch_order_for_driver(self, rest, order_id, username, auth):
        """
        Verify if the mock order created above is fetch correctly
        """
        rest.credentials(HTTP_AUTHORIZATION=auth)
        response = rest.get("/drivers/orders/" , format='json')

        assert response.data

        order_ids = []
        for sales_order in response.data["results"]:
            order_ids.append(sales_order["increment_id"])

        assert order_id in order_ids

    def test_complete_order(self, rest, auth, order_id):
        rest.credentials(HTTP_AUTHORIZATION=auth)
        response = rest.post(
                "/drivers/complete_order/",
                {"increment_id": order_id},
                format='json')

        assert response.data["status"] == True

        sales_order = models.SalesFlatOrder.objects.filter(increment_id=order_id)
        assert sales_order[0]

        sales_order = sales_order[0]
        assert sales_order.status == "complete"




