"""All product price controller related actions."""

import logging

import pandas as pd

from app.core import models as models

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ProductsPriceController(object):
    """Product Price Controller."""

    def __init__(self):
        """constructor."""
        pass

    def get_products_price(self, store_id):
        """To get current stores products prices.

        Params:
            store_id(int): selected store id


        """
        # To get CatalogProductFlat objects by storewise
        products = getattr(
            models,
            "CatalogProductFlat{}".format(store_id))

        columns = ['price', 'special_price', 'entity_id']

        #  Filter only the active and visible products
        products = products.objects.filter(status=1, visibility=4).values_list(*columns)

        # Create the DataFrame for products
        products_df = pd.DataFrame(
            list(products), columns=columns).to_dict('records')

        logger.info(
            'Fetched the products prices:{} in store{}'.format(
                products_df, store_id))

        return products_df
