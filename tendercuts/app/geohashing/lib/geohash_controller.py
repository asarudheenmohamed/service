"""Controller to process Geohash."""
import logging
import traceback
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyBgXEjOMJU2_XAnuI6mv6pREmieM639Gh8')

from ..models.geocodes import TcMapViewGeohash, StockWarehouse, StockWarehouseTcMapViewGeohashRel
from app.core.models.store import CoreStore, GmapLangandlatisLongandlatisStore

logger = logging.getLogger(__name__)


class GeohashController(object):
    """Geohash controller."""

    def get_store_id(self, geohash, lat, lng):
        """
        Returns store id if geohash matches,
        else triggers get_store_by_distance_matrix() to 
        find store id from lat,lng

        Raises Exception when geohash,lat,lng doesn`t match

        Params:
        geohash(string)
        lat(number)
        lng(number)

        Response: {'status': True, "store_id": None}
        """
        try:
            store_id = None
            geohash_map_obj = TcMapViewGeohash.objects.filter(hash_id=geohash)
            if not geohash_map_obj and (lat is None and lng is None):
                logger.warn("lat,lng is not set for address")
                raise Exception

            if not geohash_map_obj and (lat is not None and lng is not None):
                logger.info(
                    "no store found for this {} geohash, checking by lat,lng".format(geohash))
                response = self.get_store_by_distance_matrix(
                    lat, lng)
                return response

            store_warehouse_tc_map_obj = StockWarehouseTcMapViewGeohashRel.objects.filter(
                tc_map_view_geohash_id=geohash_map_obj[0].id)

            if not store_warehouse_tc_map_obj:
                logger.warn("store_warehouse_tc_map_obj not exists")
                raise Exception

            # accessing stock_warehouse table using foreign key
            store_id = CoreStore.objects.get(
                code=store_warehouse_tc_map_obj[0].stock_warehouse.mage_code).store_id

            if not store_id:
                logger.warn("not able to get store_id ")
                raise Exception

            logger.info("found store_id:{} for customer geohash:{}".format(
                store_id,
                geohash))
            response = {'status': True, "store_id": store_id}

        except Exception:
            exception = traceback.format_exc()
            logger.warn("exception caught for customer geohash:{},lat:{},lng:{},exception{}".format(
                geohash, lat, lng, exception))
            response = {'status': False, "store_id": None}
            return response

        return response

    def get_store_by_distance_matrix(self, lat, lng):
        """
        Looks up for store with lat and long,
        returns store if available within 13kms

        Params:
        lat(number)
        lng(number)

        Response: {'status': True, "store_id": None}
        """
        origin = [str(lat)+","+str(lng)]
        stores = GmapLangandlatisLongandlatisStore.objects.all()
        destinations = list(map((lambda x: str(
            x.longandlatis.latitude) + "," + str(x.longandlatis.longitude)), stores))
        logger.info("Hitting distance_matrix api")

        distance_matrix_output = gmaps.distance_matrix(
            origin, destinations, mode="driving", units="metric")
        
        logger.info("Received distance_matrix output for customer lat,lng")

        if distance_matrix_output['status'] == 'OK':
            rows = distance_matrix_output['rows'][0]['elements']
            rows = list(
                filter((lambda x: x['status'] != "ZERO_RESULTS"), rows))

            if len(rows) != 0:
                rows = list(
                    map((lambda (i, x): [x, stores[i]]), enumerate(rows)))
                rows.sort(cmp=lambda x, y: x[0]['distance']
                          ['value'] - y[0]['distance']['value'])
                distance_data, selectedStore = rows[0]

                if distance_data['distance']['value'] > 13 * 1000:
                    logger.debug("found store:{} for customer but in very long distance {}".format(
                        selectedStore.longandlatis.storename, distance_data['distance']['value']))
                    raise Exception

                logger.info("found store:{} by distance_matrix for customer lat:{}, lng:{}".format(
                    selectedStore.longandlatis.storename, lat, lng))
                return {"status": True, "store_id": selectedStore.store_id}
            logger.warn("rows length from distance matrix is 0 ")
            raise Exception
        else:
            logger.warn("distance_matrix status is not OK")
            raise Exception
