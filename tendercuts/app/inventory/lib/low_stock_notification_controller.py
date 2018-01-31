"""Low stock notification controller related actions."""
import logging

import pandas as pd

from app.core.models.inventory import GraminventoryLatest

logger = logging.getLogger(__name__)


class LowStockNotificationController(object):
    """Low Stock Notifiation Controller."""

    def __init__(self):
        """Constructor."""
        pass

    def get_low_stocks(self):
        """To get low stock products.

        Returns:
            low_stocks

        """
        # fast moving sku's in list
        fast_moving_sku = ['CHK_BIRI_CUT', 'CHK_BONELESS', 'CHK_BR_BONELESS', 'CHK_CNTRY_UNIT', 'CHK_CNTRY_WOS_UNIT', 'CHK_DRM_SKIN_OFF', 'CHK_EGG', 'CHK_LEG_SKIN_OFF', 'CHK_LOLLI', 'CHK_MINCE', 'CHK_SELECT', 'CHK_WHL_SKIN_OFF',
        'CHK_WHL_SKIN_ON', 'GT_BIRYANI_CUT', 'GT_BONELESS', 'GT_CURRY_CUT', 'GT_FAT_FREE_BONELESS', 'GT_MINCE', 'GT_REG_BONELESS', 'GT_REG_CURRY_CUT', 'MRT_CHETTINAD_CHICKEN_65', 'MRT_MASRAS_CHICKEN_65_BONELESS', 'SF_ANCHOVY',
        'SF_BABY_SEER', 'SF_BLUE_CRAB', 'SF_BPOMFRET', 'SF_CATLA', 'SF_CATLA_SMALL', 'SF_EMPEROR', 'SF_FWPOMFRET', 'SF_IM', 'SF_INDIAN_SALMON', 'SF_LADY_FISH', 'SF_MATHI', 'SF_PRAWN', 'SF_ROHU', 'SF_ROHU_SMALL', 'SF_SANKARA',
        'SF_SEABASS', 'SF_SEER', 'SF_SHARK', 'SF_SHELLA', 'SF_TREVLLY', 'SF_TUNA']

        columns = ['product_id', 'product__sku', 'store_id', 'qty']

        logger.debug(
            "To get products which is less than 5 and create DaraFrame with columns: {}".format(
                columns))

        inventory_objs = GraminventoryLatest.objects.select_related(
            'product').filter(product__sku__in=fast_moving_sku, qty__lte=5).values_list(*columns)

        if not inventory_objs:
            raise ValueError("Fast moving sku's are InStock")
        # create DataFrame with our above mentioned columns
        inventory_df = pd.DataFrame(list(inventory_objs), columns=columns)

        low_stocks = {}

        def format_df(group):
            store_id = group.store_id.tolist()[0]
            #  To change DataFrame into Dictionary format
            low_stocks[store_id] = group[['product_id', 'product__sku', 'qty']].to_dict('records')

        # To group our Dataframe with store_id
        inventory_df.reset_index().groupby('store_id').apply(format_df)

        logger.info(
            "Grouped the DataFrame with store_id and changed it into Dictionary format: {}".format(
            low_stocks))

        return low_stocks
