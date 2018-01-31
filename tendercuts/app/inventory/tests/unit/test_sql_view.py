import pytest
from app.core.models import GraminventoryLatest, Graminventory
import datetime

@pytest.mark.django_db
class _TestDpInventory:
    """
    271 (Breast Raw mat) -> 199 (B.Boneless)
    199 -> 380 GPU
    """

    def setUp(self):
        """Sets up the zero inv for parent."""
        Graminventory.objects.update_or_create(
            date=format(datetime.datetime.today(), "%Y-%m-%d"),
            product_id=271,
            store_id=4,
            defaults={
                'qty': 0,
                'forecastqty': 0

            }
        )


    @pytest.mark.parametrize("product_id,store_id,qty,forecast,expected_qty,expected_sch", [
        (199, 4, 100, 100, 263, 263),  # fetch express and scheduled
        (199, 4, 100, 0, 263, 0),  # fetch express
        (199, 4, 0, 100, 0, 263),  # fetch express
    ])
    def test_express(self, product_id, store_id, qty, forecast, expected_qty, expected_sch):
        """Assert express inve"""
        Graminventory.objects.update_or_create(
            date=format(datetime.datetime.today(), "%Y-%m-%d"),
            product_id=product_id,
            store_id=store_id,
            defaults={
                'qty': qty,
                'forecastqty': forecast}
        )

        inv = GraminventoryLatest.objects.filter(product_id=product_id, store_id=store_id)
        assert len(inv) == 1
        assert inv[0].qty == expected_qty
        assert inv[0].scheduledqty == expected_sch



@pytest.mark.django_db
class _TestOmniInventory:
    """
    271 (Breast Raw mat) -> 199 (B.Boneless)
    199 -> 380 GPU
    """

    @pytest.mark.parametrize("child,parent,expected_qty,expected_sch", [
        ((199, 1, 100, 0), (271, 1, 100, 0), 465, 465), # 1,0 (263 + 202) -- no expiring
        ((199, 1, 100, 25), (271, 1, 100, 25), 465, 347),  # 1,0 (197 + 150) -- has expiring
        # only child test cases
        ((199, 1, 100, 25), (271, 1, 0, 0), 263, 197), # 1,0 (197, 189) # BUG on ratio is not applied
        # only parent -- this means that the inv is only for delivery
        # automatically switches off to DP mode
        ((199, 1, 0, 0), (271, 1, 100, 25), 202, 149), # 1,0
        #o.o.s
        ((199, 1, 0, 0), (271, 1, 0, 0), 0, 0),

    ])
    def test_express(self, child, parent, expected_qty, expected_sch):
        """Assert express inve"""
        for inv in [child, parent]:
            Graminventory.objects.update_or_create(
                date=format(datetime.datetime.today(), "%Y-%m-%d"),
                product_id=inv[0],
                store_id=inv[1],
                defaults={
                    'qty': inv[2],
                    'expiringtoday': inv[3]}
            )

        product_id, store_id, _, _ = child
        inv = GraminventoryLatest.objects.filter(product_id=product_id, store_id=store_id)

        assert len(inv) == 1
        assert inv[0].qty == expected_qty
        assert inv[0].scheduledqty == expected_sch

