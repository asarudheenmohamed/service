
import logging


from app.core.models.entity import EavAttribute
from app.core.models.customer import address
from app.driver.lib.end_of_day_driver_status import DriverStatusController

logger = logging.getLogger(__name__)


class CustomerLocationController(object):
    """Driver controller."""

    def __init__(self):
        """Constructor."""
        pass

    def update_customer_location(self, customer_id, lat, lon):
        """Update customer current location.

        Params:
         customer_id(int):user entity_id
         lat(int):custoner location latitude
         lon(int):customer location longitude

        """
        customer_address_obj = address.CustomerAddressEntity.objects.filter(
            parent__entity_id=customer_id)[0]

        for loc_value in ['latitude', 'longitude']:

            eav_obj = EavAttribute.objects.filter(attribute_code=loc_value)[0]
            customer_addressentity_obj = address.CustomerAddressEntityText.objects.filter(
                attribute=eav_obj, entity=customer_address_obj)

            if customer_addressentity_obj:
                customer_addressentity_obj = customer_addressentity_obj[0]
                customer_addressentity_obj.value = lat if loc_value == 'latitude' else lon
                customer_addressentity_obj.save()
                logger.info(
                    'Update the current location lat:{} and long:{} for the customer:{}'.format(
                        lat, lon, customer_id))
            else:
                customer_addressentity_obj = address.CustomerAddressEntityText.objects.create(
                    attribute=eav_obj,
                    entity_type_id=2,
                    entity=customer_address_obj,
                    value=lat if loc_value == 'latitude' else lon)
                logger.info(
                    'Create a currnt location lat:{} and long:{} for the customer:{}'.format(
                        lat, lon, customer_id))

        return customer_addressentity_obj
