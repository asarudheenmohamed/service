"""All product price controller related actions."""

import logging
import datetime

import pandas as pd
import numpy as np
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

        columns = ['price', 'special_price', 'entity_id', 'special_to_date']

        #  Filter only the active and visible products
        products = products.objects.filter(
            status=1, visibility=4).values_list(*columns)

        # Create the DataFrame for products
        products_df = pd.DataFrame(
            list(products), columns=columns)
        products_df.special_to_date = pd.to_datetime(products_df.special_to_date)

        products_df.special_price = np.where(
            products_df.special_to_date > datetime.datetime.now(), products_df.special_price, None)
        products_df = products_df[[
            'price', 'special_price', 'entity_id']].to_dict('records')

        return products_df
