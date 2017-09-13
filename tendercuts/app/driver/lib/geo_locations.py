"""End point for the return user location address."""
from geolocation.main import GoogleMaps
from django.conf import settings


class GeoLocations:
    """Geo locations controller."""

    def __init__(self):
        """Initialize the Google map Api object."""
        self.google_maps = GoogleMaps(
            api_key=settings.GOOGLEMAP['key'])

    def get_location(self, lat, lng):
        """Get location for the user base latitude and longitude.

        Params:
            lat(str): location latitude id
            lng(str): location longitude id

        Returns:
         return a location address

        """
        location = self.google_maps.search(lat=lat, lng=lng).first()

        return location.formatted_address
