from rest.lib.models.point import MapPoint, Order

class TestMapPoint:
    def test_cart_cords(self):
        pt = MapPoint(12.92908, 77.62187900000004)
        assert pt.x == 1331.4968240156854
        assert pt.y == 6067.040548048426
        assert pt.z == 1425.925732979244

    def test_cart_cords_2(self):
        pt = MapPoint(12.930011939588985, 77.62474358081818)
        print(pt.x, pt.y, pt.z)
        assert pt.x == 1331.188521557925
        assert pt.y == 6067.084455291711
        assert pt.z == 1426.0267642755234


class TestOrder:
    def test_order(self):
        pt = Order(1, 12.92908, 77.62187900000004)
        assert pt.id == 1
        assert pt.x == 1331.4968240156854
        assert pt.y == 6067.040548048426
        assert pt.z == 1425.925732979244

        assert pt.is_assigned is False
        pt.assign_route(self)
        assert pt.is_assigned is True
