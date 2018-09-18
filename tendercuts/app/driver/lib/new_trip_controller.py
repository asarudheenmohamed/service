from app.driver.models import DriverTrip
from app.core.models import SalesFlatOrder


class DriverTripController(object):
    """New version of trip controller without the caching."""
    trip = None  # type: DriverTrip
    TRIP_CREATED = 0
    TRIP_PROGRESS = 1
    TRIP_COMPLETE = 2

    @classmethod
    def get_or_create_trip(cls, user):
        """Search for any active trip or create a new
        trip."""

        trip = DriverTrip.objects.filter(
            driver_user=user,
            status__in=[cls.TRIP_CREATED, cls.TRIP_PROGRESS])

        if len(trip) > 0:
            trip = trip.first()

            controller = cls(trip)  # type: DriverTripController

            if controller.is_trip_stale():
                # check if the trip has been completed via external (mage, external)
                trip.status = cls.TRIP_COMPLETE
                trip.save()
            else:
                return trip

        return DriverTrip.objects.create(
            driver_user=user, status=cls.TRIP_CREATED)

    @classmethod
    def get_completed_trips(cls, user):
        """Get all completed trips

        :param user:
        :return:
        """
        return DriverTrip.objects.filter(
            driver_user=user,
            status=cls.TRIP_COMPLETE)

    def __init__(self, trip):
        self.trip = trip

    def start_trip(self):
        """Begins the trip"""
        self.trip.status = 1
        self.trip.save()

    def is_trip_stale(self):
        """A trip is considered stale, if all orders in the trip are in one
        of the termination states

        :return: bool
        """
        order_ids = self.trip.driver_order.values_list('increment_id', flat=True)

        # if there are no orders in the trip, it means this is a new tip
        if len(order_ids) == 0:
            return False

        orders = SalesFlatOrder.objects \
            .filter(increment_id__in=list(order_ids),
                    status__in=['cancelled', 'closed', 'complete']) \
            .values_list('increment_id', 'status')

        # if all orders in the trip are in closing states, then we
        # consider it as stale state
        if len(orders) == len(order_ids):
            return True

        return False
