
def test_orders(rest):
    orders =rest.get("/sale_order/orders/?user_id={}".format(
        18963), format='json')
    assert len(orders.data['results']) == 5
