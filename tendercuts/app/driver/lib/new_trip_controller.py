from app.driver.models import DriverTrip
from app.core.models import SalesFlatOrder
from app.driver.lib.google_api_controller import GoogleApiController
from app.driver.models import (DriverOrder, DriverPosition, DriverTrip,
                               OrderEvents)


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
            order_ids = trip.driver_order.values_list(
                'increment_id', flat=True)

            # if there are no orders in the trip, it means this is a new tip
            if len(order_ids) == 0:
                return trip

            orders = SalesFlatOrder.objects\
                .filter(increment_id__in=list(order_ids),
                        status__in=['out_delivery', 'processing']) \
                .values_list('increment_id', 'status')

            if len(orders) != 0:
                return trip
            else:
                # check if the trip has been completed via external (mage,
                # external)
                trip.status = cls.TRIP_COMPLETE
                trip.save()

        return DriverTrip.objects.create(
            driver_user=user, status=cls.TRIP_CREATED)

    def check_and_complete_trip(self):
        """Check if the trip can be completed.

        :param trip: DriverTrip
        :return: DriverTrip or None if completed

        """
        # check if all orders are complete.
        order_ids = trip.driver_order.values_list('increment_id', flat=True)

        orders = SalesFlatOrder.objects.filter(increment_id__in=list(order_ids),
                                               status__in=['out_delivery', 'processing']) \
            .values_list('increment_id', 'status')

        if not orders:
            trip.status = self.TRIP_COMPLETE
            trip.save()
            self.compute_driver_trip_distance()

    def create_sequence_number(self):
        """create sequence number for the driver assigned order."""
        order_ids = list(
            trip_obj.driver_order.all().values_list(
                'increment_id', flat=True))

        order_objects = SalesFlatOrder.objects.filter(
            increment_id__in=order_ids)

        for index, value in enumerate(order_ids, start=1):
            # update order sequence number
            order.sequence_number = index
            order = order_objects.get(increment_id=value)
            order.save()

    def update_sequence_number(self, order_id, sequence_number):
        """Update order sequence number for the given order id.

        Params:
            order_id(str): order increment_id
            sequence_number(str): order sequence number

        """
        trip_obj = DriverTrip.objects.get(
            driver_order__increment_id=order_id)
        order_ids = list(
            trip_obj.driver_order.all().values_list(
                'increment_id', flat=True))

        order_objects = SalesFlatOrder.objects.filter(
            increment_id__in=order_ids,
            sequence_number__gte=sequence_number)
        order_ids = list(order_objects.values_list(
            'increment_id', flat=True).order_by('sequence_number'))

        # for the given order id moves to last index
        order_ids.append(order_ids.pop(order_ids.index(order_id)))
        for index, value in enumerate(order_ids, start=sequence_number):
            order = order_objects.get(increment_id=value)
            # order.sequence_number = index
            order.save()

    def _get_way_points(self, trip_starting_time,
                        order_event_complete_objects, driver_user):
        """"""
        way_points = []

        for event_complete_object in order_event_complete_objects:

            # fetch driver position
            position_objects = DriverPosition.objects.filter(
                driver_user=driver_user, recorded_time__range=(
                    trip_starting_time, event_complete_object.updated_time))
            # mid index of driver position
            mid_index = len(position_objects) / 2
            # mid position
            try:
                mid_position = position_objects[mid_index]
                way_points.append(str(mid_position))
                way_points.append(str(event_complete_objec))
            except:
                pass

            trip_starting_time = event_complete_object.updated_time

        return way_points

    def _split(self, waypoints, index):
        """Split the waypoints based on index."""
        ways = []
        while len(waypoints) > index:
            pice = waypoints[:index]

            ways.append(pice)
            waypoints = waypoints[index:]
        ways.append(waypoints)

        return ways

    def compute_driver_trip_distance(self):
        """Update the km taken by the driver for each trip.

        Params:
           trip(obj): completed driver trip object

        """
        # based on lat long distance has been measured for each trip taken by
        # the driver

        # driver trip starting point

        order_events = OrderEvents.objects.filter(driver__in=self.trip.driver_order.all(
        )).prefetch_related('driver_position').order_by('updated_time')

        # starting and ending destination point
        starting_points = str(order_events.first().driver_position)
        destination_point = str(order_events.last().driver_position)

        # trip starting point
        trip_starting_time = order_events.first().updated_time

        # sort completed order only because we get a order completed
        # location and completed time
        order_event_complete_objects = order_events.filter(
            status='completed').order_by('updated_time')

        way_points = self._get_way_points(
            trip_starting_time, order_event_complete_objects, self.trip.driver_user)

        split_way = self._split(way_points, 22)

        km_travelled = 0

        for waypoints in split_way:
            try:
                destination = waypoints[-1]
            except IndexError:
                destination = destination_point

            directions = GoogleApiController(None).get_directions(
                starting_points, destination_point, waypoints=waypoints)

            distance = directions[0]['legs'][0]['distance']['value']

            km_travelled += distance

            starting_point = destination

        self.trip.km_travelled = km_travelled

        self.trip.save()

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
