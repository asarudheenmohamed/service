"""Controller to process Geohash."""
import logging
import traceback
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyBgXEjOMJU2_XAnuI6mv6pREmieM639Gh8')

from ..models.geocodes import  TcMapViewGeohash, StockWarehouse, StockWarehouseTcMapViewGeohashRel
from app.core.models.store import CoreStore,GmapLangandlatisLongandlatisStore

logger = logging.getLogger(__name__)


class GeohashController(object):
    """Geohash controller."""

    def __init__(self):
        """Constructor."""
        pass

    def get_store_mage_code(self,geohash,lat,lng):
        """
        Returns store code if geohash matches,
        else triggers getStoreFromPathString() to 
        find store code from lat,lng

        Raises Exception when geohash,lat,lng doesn`t match
        """

        try:
            geohash_map_obj = TcMapViewGeohash.objects.filter(hash_id=geohash)
            if len(geohash_map_obj) == 0:
                if (lat != None) and (lng != None):
                    logger.info("no store found for this {} geohash, checking by lat,lng".format(geohash))
                    response = self.get_store_by_distance_matrix(lat,lng,"get_store_mage_code")
                    return response
                else:
                    logger.warn("lat, lng is not set for this address")
                    return None
            store_warehouse_tc_map_obj = StockWarehouseTcMapViewGeohashRel.objects.filter(tc_map_view_geohash_id=geohash_map_obj[0].id)
            
            #accessing stock_warehouse table using foreign key
            response = {
                 'status': True,
                 "store_name" : store_warehouse_tc_map_obj[0].stock_warehouse.mage_code
                 }

            logger.info("found store:{} for customer geohash:{}".format(
                store_warehouse_tc_map_obj[0].stock_warehouse.mage_code,
                geohash
                ))

        except Exception:
            exception = traceback.format_exc()
            logger.warn("customer geohash:{},lat:{},lng:{} didnot match our entries in db, and caused exception{}".format(geohash,lat,lng,exception))
            response = { 'status': False,"store_name": None}
            return response
        
        return response

    def get_store_id(self,geohash,lat,lng):
        """
        Returns store id if geohash matches,
        else triggers getStoreFromPathString() to 
        find store id from lat,lng

        Raises Exception when geohash,lat,lng doesn`t match

        """
        try:
            store_id = None
            geohash_map_obj = TcMapViewGeohash.objects.filter(hash_id=geohash)
            if len(geohash_map_obj) == 0:
                if (lat != None) and (lng != None):
                    logger.info("no store found for this {} geohash, checking by lat,lng".format(geohash))
                    response = self.get_store_by_distance_matrix(lat,lng,"get_store_id")
                    return response
                else:
                    logger.warn("lat, lng is not set for this address")
                    return None
            store_warehouse_tc_map_obj = StockWarehouseTcMapViewGeohashRel.objects.filter(tc_map_view_geohash_id=geohash_map_obj[0].id)

            #accessing stock_warehouse table using foreign key
            store_id = CoreStore.objects.get(code=store_warehouse_tc_map_obj[0].stock_warehouse.mage_code).store_id

            logger.info("found store:{} for customer geohash:{}".format(
                store_warehouse_tc_map_obj[0].stock_warehouse.mage_code,
                geohash))

        except Exception:
            store_id = None
            exception = traceback.format_exc()
            logger.warn("customer geohash:{},lat:{},lng:{} didnot match our entries in db, and caused exception{}".format(geohash,lat,lng,exception))
            return store_id
        
        return store_id
        


    def get_store_by_distance_matrix(self,lat,lng,mode):
        """
        Looks up for store with lat and long,
        returns store if available
        """
        origin = [str(lat)+","+str(lng)]
        stores = GmapLangandlatisLongandlatisStore.objects.all()
        destinations = list(map((lambda x: str(x.longandlatis.latitude)+ "," + str(x.longandlatis.longitude)), stores))
        distance_matrix_output = gmaps.distance_matrix(origin,destinations,"driving","","","metric")

        if distance_matrix_output['status'] == 'OK':
            rows = distance_matrix_output['rows'][0]['elements']
            rows = list( filter((lambda x: x['status'] != "ZERO_RESULTS"), rows))

            if len(rows) != 0:
                rows = list(map((lambda (i,x): [x,stores[i]] ), enumerate(rows)))
                rows.sort(cmp=lambda x, y: x[0]['distance']['value'] - y[0]['distance']['value'])
                distance_data, selectedStore = rows[0]

                if distance_data['distance']['value'] > 13 * 1000:
                    logger.debug("found store:{} for customer but in very long distance {}".format(selectedStore.longandlatis.storename,distance_data['distance']['value']))
                    raise Exception

                logger.info("found store:{} by distance_matrix for customer lat:{}, lng:{}".format(selectedStore.longandlatis.storename,lat,lng))
                if mode == "get_store_id":
                    return selectedStore.store_id
                else:
                    return {"status": True,"store_name":selectedStore.longandlatis.storename }
            raise Exception
        else:
            logger.warn("distance_matrix status is not OK")
            raise Exception
