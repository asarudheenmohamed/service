from app.driver.models import DriverTrip


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
            return trip.first()

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
