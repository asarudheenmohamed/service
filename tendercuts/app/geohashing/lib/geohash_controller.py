"""Controller to process Geohash."""
import logging

import googlemaps
from app.core.models.store import CoreStore, GmapLangandlatisLongandlatisStore
from app.geohashing import tasks
from django.conf import settings

from ..models.geocodes import (StockWarehouseTcMapViewGeohashRel,
                               TcMapViewGeohash)

logger = logging.getLogger(__name__)


class NoStoreFoundException(Exception):
    pass


class GeohashController(object):
    """Geohash controller."""

    DISTANCE_THRESHOLD = 8

    def __init__(self):
        self.gmaps = googlemaps.Client(key=settings.GOOGLE_MAP_DISTANCE_API['KEY'])

    def get_store_id(self, geohash, lat, lng):
        """
        Returns store id if geohash matches,
        else triggers get_store_by_distance_matrix() to 
        find store id from lat,lng

        Raises Exception when geohash,lat,lng doesn`t match

        Params:
        geohash(string): geohash of customer address
        lat(number): latitude of customer address
        lng(number): longitude of customer address

        Returns:
            store_id

        Raises:
            NoStoreFound exception
        """
        store_id = None

        geohash_map_obj = TcMapViewGeohash.objects.filter(hash_id=geohash)

        if not geohash_map_obj and (lat is None and lng is None):
            return NoStoreFoundException()

        # Fallback: In case no relevant geohash is found, then fallback
        # to the previous logic of using lat and lng
        if not geohash_map_obj and (lat is not None and lng is not None):
            logger.info(
                "no store found for this {} geohash, checking by lat,lng".format(geohash))
            return self._get_store_by_distance_matrix(geohash, lat, lng)

        store_warehouse_tc_map_obj = StockWarehouseTcMapViewGeohashRel.objects.filter(
            tc_map_view_geohash_id=geohash_map_obj[0].id)

        if not store_warehouse_tc_map_obj:
            raise NoStoreFoundException()

        # accessing stock_warehouse table using foreign key
        store_id = CoreStore.objects.get(
            code=store_warehouse_tc_map_obj[0].stock_warehouse.mage_code).store_id

        if not store_id:
            raise NoStoreFoundException

        logger.info("found store_id:{} for customer geohash:{}".format(
            store_id,
            geohash))

        return store_id

    def _get_store_by_distance_matrix(self, geohash, lat, lng):
        """
        Looks up for store with lat and long,
        returns store if available within 13kms

        Params:
        lat(number)
        lng(number)

        Returns:
            store_id

        Raises:
            NoStoreFound exception

        """
        origin = [str(lat) + "," + str(lng)]

        stores = GmapLangandlatisLongandlatisStore.objects.all()

        destinations = list(map((lambda x: str(
            x.longandlatis.latitude) + "," + str(x.longandlatis.longitude)), stores))

        distance_matrix_output = self.gmaps.distance_matrix(
            origin, destinations, mode="driving", units="metric")

        if distance_matrix_output['status'] != 'OK':
            raise NoStoreFoundException()

        """
        "rows": [
            {
                "elements": [
                    {
                        "distance": {
                            "text": "41.5 km",
                            "value": 41509
                            },
                        "status": "OK"
        """
        rows = distance_matrix_output['rows'][0]['elements']
        rows = list(filter((lambda row: row['status'] != "ZERO_RESULTS"), rows))

        if len(rows) == 0:
            raise NoStoreFoundException()

        # joining distance_output with stores, store is as (store, distance)
        stores_with_distance = []
        for index, row in enumerate(rows):
            stores_with_distance.append((stores[index], row['distance']['value']))

        # sorting stores by distance in ascending order
        stores_with_distance.sort(cmp=lambda store_a, store_b: store_a[1] - store_b[1])

        # stripping off nearest store`s distance_data and store details
        selectedStore, distance = stores_with_distance[0]

        if distance > self.DISTANCE_THRESHOLD * 1000:
            raise NoStoreFoundException()

        msg = 'Geohash:{}, Latitude:{}, Longitude:{}, Store by distance matrix'.format(
                    geohash, lat, lng)

        tasks.geohash_mail.delay(msg)

        return selectedStore.store_id
