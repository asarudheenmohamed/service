"""Endpoint for the finding store mage_code with geohash,lat,lng."""

import logging

from rest_framework.views import APIView
from rest_framework.response import Response
from ..lib.geohash_controller import GeohashController



class GeohashToStore(APIView):
    """
    Params:
    geohash,lat,lng

    url: geohash/store
    """  
    def post(self, request, format=None):

        controller = GeohashController()
        geohash = request.data["geohash"]
        lat = request.data["lat"]
        lng = request.data["lng"]
        status = controller.get_store_id(geohash,lat,lng)

        return Response(status)