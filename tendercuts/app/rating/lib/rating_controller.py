"""Rating Controller."""

import logging

from app.core.lib.communication import FreshDesk
from app.core.lib.user_controller import CustomerSearchController
from app.core.lib.utils import get_mage_userid
from app.core.models import SalesFlatOrder
from app.rating.models import Rating

logger = logging.getLogger(__name__)


class RatingController(object):
    """Rating controller."""

    def __init__(self, order_id):
        """Constructor."""
        self.order_id = order_id

    def get_userid(self):
        """To get the user_id.

        params:
           order_id (obj): sale order increment_id

        """
        rating_obj = Rating.objects.filter(increment_id=self.order_id).last()

        # get megento user id
        user_id = get_mage_userid(rating_obj.customer)

        return user_id

    def create_fresh_desk_ticket(self):
        """Create fresh desk ticket for the given order-rating.

        params:
           order_id (obj): sale order increment_id

        """
        user_id = get_userid()
        # fetch the customer basic info
        customer_details = CustomerSearchController.load_basic_info(
            user_id)

        subject = "#{} Customer Review&Rating".format(self.order_id)

        tags = ", ".join(
            str(tag) for tag in rating_obj.rating_tag.values_list(
                'tag_name', flat=True))

        description = "Order Id #{} Comments:{} Review Rating:{} Rating Tags:{}".format(
            self.order_id, rating_obj.comments, rating_obj.rating, tags)

        ticket_obj = FreshDesk().create_ticket(
            subject, description, customer_details[1], customer_details[2])

        logger.info(
            'FreshDesk ticket created, customer rating:{} for the order:{}'.format(user_id, self.order_id))

        return ticket_obj

    def update_rating(self, rating):
        """Rating updated in sale order obj.
        Params:
            increment_id(int): order id
            rating(int): customer rating
        """
        obj = SalesFlatOrder.objects.filter(
            increment_id=self.order_id).update(
            rating=rating)

        return obj

    @classmethod
    def fetch_customer_last_order(cls, user_id):
        """Return the customer last order."""
        order = SalesFlatOrder.objects.filter(
            customer_id=user_id, status='complete').last()

        logger.info(
            'Fetched the customer:{} last order:{}'.format(user_id, order.increment_id))

        return order



    def check_five_star_rating(self):
        """Check user gives five star rating consecutively or not.

        """
        user_id = get_userid()

        queryset = SalesFlatOrder.objects \
               .filter(customer_id=user_id, status='complete') \
               .order_by('-created_at') \
               .prefetch_related("items") \
               .prefetch_related("payment") \
               .prefetch_related("shipping_address")[:2]

        if queryset.length > 2:
            if (queryset[0].rating == 5 and queryset[1] == 5):
                return True
            else:
                return False
        else:
            return False

    
