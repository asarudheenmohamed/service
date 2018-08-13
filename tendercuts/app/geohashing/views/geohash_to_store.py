"""Endpoint for the finding store mage_code with geohash,lat,lng."""

import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from ..lib.geohash_controller import GeohashController, NoStoreFoundException


class GeohashToStore(APIView):
    """
    Converts geohash to store_id. If geohash doesn`t
    work, then computes distance matrix for lat,lng
    and returns the corresponding store_id.
    """

    def post(self, request, format=None):
        """
        Params:
        geohash(string): Geohash of customer address
        lat(number): Latitude of customer address
        lng(number): Longitude of customer address

        Url: geohash/store

        Returns: 
        {'status': Boolean, "store_id": True}
        """

        geohash = request.data["geohash"]
        lat = request.data["lat"]
        lng = request.data["lng"]

        controller = GeohashController()
        store_id = None
        status = True
        try:
            store_id = controller.get_store_id(geohash, lat, lng)
        except NoStoreFoundException:
            status = False

        return Response({'status': status, "store_id": store_id})
