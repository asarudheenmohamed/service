from app.core.models import SalesFlatOrder

import abc
import datetime
import pytz
import collections


class Delivery:

    @abc.abstractproperty
    def cost(self):
        pass

    @abc.abstractmethod
    def is_slots_available(self):
        pass

    @property
    def tz(self):
        return pytz.timezone('Asia/Kolkata')


class ScheduledDelivery(Delivery):
    DAYS = 2
    CUT_OFF = 3  # hours
    SLOTS = [
        (datetime.time(7, 0, 0), {"ddate_id": 52, "interval": "7:00 - 9:00"}),
        (datetime.time(9, 0, 0), {"ddate_id": 53, "interval": "9:00 - 11:00"}),
        (datetime.time(11, 0, 0), {
         "ddate_id": 54, "interval": "11:00 - 13:00"}),
        (datetime.time(17, 0, 0), {
         "ddate_id": 55, "interval": "17:00 - 19:00"}),
        (datetime.time(19, 0, 0), {
         "ddate_id": 56, "interval": "19:00 - 21:00"}),
    ]

    @property
    def cost(self):
        return 29

    def is_slots_available(self):
        return True

    def available_slots(self, now=None):
        slots = collections.defaultdict(list)
        now = now or datetime.datetime.now(tz=self.tz)

        for i in range(self.DAYS):
            date = datetime.datetime.now(
                tz=self.tz) + datetime.timedelta(days=i)

            for time, slot_desc in self.SLOTS:
                slot_cutoff = date.replace(
                    hour=time.hour,
                    minute=time.minute)

                seconds_left = (slot_cutoff - now).total_seconds()

                if seconds_left > 3600 * self.CUT_OFF:
                    slots[format(date, "%Y-%m-%d")].append(slot_desc)

        slots = [{"date": date, "times": times}
                 for date, times in slots.items()]

        return slots

    def serialize(self):
        data = {}
        data["name"] = "Scheduled Delivery"
        data["cost"] = self.cost
        data["is_available"] = self.is_slots_available()
        data["available_slots"] = self.available_slots()

        return data


class ExpressDelivery(Delivery):

    @property
    def cost(self):
        return 49

    def time_in_range(self, start, end, x):
        """Return true if x is in the range [start, end]"""
        return start <= x <= end

    def is_slots_available(self, now=None):
        start = datetime.time(6, 30, 0, tzinfo=self.tz)
        end = datetime.time(20, 0, 0, tzinfo=self.tz)
        now = now or datetime.datetime.now(tz=self.tz).time()

        return self.time_in_range(start, end, now)

    def serialize(self):
        data = {}
        data["name"] = "Express Delivery"
        data["cost"] = self.cost
        data["is_available"] = self.is_slots_available()
        data["available_slots"] = []
        # Hack for the bug in mobile app
        if not self.is_slots_available():
            data = {}

        return data
