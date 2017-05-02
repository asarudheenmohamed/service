
def test_orders(auth_rest):
    orders = auth_rest.get("/sale_order/orders/?user_id={}".format(
        18963), format='json')
    print (orders)
    assert len(orders.data['results']) == 10
