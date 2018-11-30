import logging
import json
import requests
import pandas as pd
import numpy as np

from bs4 import BeautifulSoup

import tempfile

import csv
import mimetypes
import os
import smtplib
import sys
import tempfile
from email import encoders
from email.message import Message
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings
from email.utils import COMMASPACE, formatdate


import pandas as pd
# from odoo import api, fields, models
# from odoo.addons.tendercuts.lib.sale_sync import commands
from pandas.compat import StringIO
# from app.core.lib.communication import Mail


logger = logging.getLogger(__name__)


def f2h_report():
    """To get data from F2H.

    Returns:
        data_F2H

    """
    product_url = "https://www.freshtohome.com/xmlconnect/product/getAllProducts"
    res = requests.get(product_url)
    master_data = res.json()

    price_url = "https://www.freshtohome.com/xmlconnect/product/getAvailableProducts"
    res = requests.get(price_url)
    price_master = res.json()

    F2H_list = []
    for product in price_master['products']:
        # import pdb
        # pdb.set_trace()
        F2H_list.append((
            product['entity_id'],
            product['price'],
            product['qty_increments']
        ))
    # import pdb
    # pdb.set_trace()
    #  create dataframe for F2H and master
    df = pd.DataFrame(
        F2H_list,
        columns=[
            "f2h_entity_id",
            "f2h_price",
            "f2h_weight"])
    b = []
    for product in master_data['products']:
        # import pdb
        # pdb.set_trace()
        b.append((
            product['entity_id'],
            product['name'],
        ))
    # import pdb
    # pdb.set_trace()
    master_df = pd.DataFrame(
        b,
        columns=[
            "f2h_entity_id", 'f2hname', ])

    import pdb
    pdb.set_trace()
    F2H_df = pd.merge(
        master_df,
        df,
        on='f2h_entity_id')

    return F2H_df
    # F2H_df.to_csv('f2h.csv', encoding='utf-8', index=False)

    # master_df = pd.DataFrame.from_csv(
    #     "~/services/tendercuts/app/sale_order/lib/master.csv")
    # master_df = pd.read_excel("/home/asarudheen/Downloads/ProductID.xlsx")
    # master_df = pd.DataFrame(master_df)
    # #  fill null values as 0 and change type to integer
    # master_df['Fresh_to_Home'] = master_df[
    #     'Fresh to Home'].fillna(0).astype(int)
    # df['f2h_id'] = df['f2h_id'].fillna(0).astype(int)
    # #  merge F2H and master dataframe to get only matched rows
    # F2H_df = df.merge(
    #     master_df,
    #     left_on='f2h_id',
    #     right_on='Fresh_to_Home',
    #     how='inner')
    # #  convert price per kg
    # F2H_df.f2h_price = F2H_df.f2h_price.astype(
    #     float) / F2H_df.f2h_weight.astype(float)

    # return F2H_df[["SKU_NAME", "f2h_id", "f2h_price"]]


def licious_report():
    """To get data from licious.

    Returns:
        data_licious

    """
    session = requests.session()

    # extract token
    data = session.get("https://m.licious.in/chicken")
    soup = BeautifulSoup(data.content)
    csrf_token = soup.find('meta', {"name": "_token"})['content']

    licious_master = []
    for cat_id in [1, 2, 3]:
        data = session.post(
            "https://m.licious.in/checkout_oos/get-products",
            data={"cat_id": cat_id},
            headers={
                "X-CSRF-TOKEN": csrf_token,
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://m.licious.in/chicken",
                "Origin": "https://m.licious.in",
                'User-Agent': 'Mozilla/5.0'
            })
        for product in data.json()['data']:

            licious_master.append((
                product['product_master']['product_id'],
                product['product_master']['pr_name'],
                product['product_pricing']['base_price'],
                product['product_master']['gross'],
                product['product_master']['pr_weight']

            ))
    # import pdb
    # pdb.set_trace()
    licious_df = pd.DataFrame(
        licious_master,
        columns=[
            "licious_id",
            "licious_name",
            "licious_price",
            "licious_weight",
            "lisious_net"])
    # licious_df.licious_price = licious_df.licious_price / (
    #     np.where(
    #         licious_df.licious_weight.str.contains('gm'),
    #         licious_df.licious_weight.str.extract('(\d+)').astype(int),
    # licious_df.licious_weight.str.extract('(\d+)').astype(int))) * 1000

    # import pdb
    # pdb.set_trace()
    return licious_df
    # df = pd.DataFrame(licious_master, columns=[])
    # licious_df.to_csv('licious.csv', encoding='utf-8', index=False)


def bigbasket_report():
    """To get data from bigbasket.

    Returns:
        data_bigbasket

    """
    bb_mutton_and_lamp_url = "https://www.bigbasket.com/custompage/sysgenpd/?type=pc&slug=mutton-lamb&sid=hm9f6YqhYwGibmbDomNjqDQ5NHwxNDM2omFvwqJ1csKiYXDDomx0zQ_ioW-qcG9wdWxhcml0eaJkc2ajbXJpAQ=="
    bb_database = "https://www.bigbasket.com/product/get-products/?slug={}&page={}&tab_type=[%22all%22]&sorted_on=popularity&listtype=pc"
    session = requests.Session()

    # acquire cookies
    data = session.get("https://www.bigbasket.com/pb/fresho-meat/?nc=fapd")
    # df['a'] = df['a'].apply(lambda x: '<a href="http://example.com/{0}">link</a>'.format(x))
    i = 1
    master = []
    for i in ["eggs-meat-fish", "mutton-lamb", "fish-seafood", "fresh-fish"]:
        # print
        # 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        # {}'.format(i)
        for page_ in xrange(1, 7):
            page = session.get(bb_database.format(i, page_))
            # import pdb
            # pdb.set_trace()
            # info = page.json()['response']['tab_info'][0]['product_info']
            # info = page.json()['tab_info'][0]['product_info']
            info = page.json()['tab_info']['product_map']["all"]["prods"]
            # tot_pages = info['tot_pages']

            # while i <= int(tot_pages):
            #     print("Running Page {}".format(i))
            #     if i != 1:
            #         page = session.get(bb_database.format(i))
            #         info = page.json()['response']['tab_info'][0]['product_info']
            # import pdb
            # pdb.set_trace()

            # print info, 'IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIi'
            for product in info:
                master.append((
                    product['sku'],
                    product['p_desc'],
                    product['sp'],
                    product['w']
                ))
            # next page
            # i += 1
    import pdb
    pdb.set_trace()
    #  create dataframe for Bigbasket and master
    df = pd.DataFrame(
        master,
        columns=[
            "bb_id",
            "bb_name",
            "bb_price",
            "bb_weight"])
    return df
    # import pdb
    # pdb.set_trace()
    # return df
    # writer = pd.ExcelWriter('product_prices.xlsx', engine='xlsxwriter')
    # df.to_excel(writer, sheet_name='big_basket_price')
    # df.to_csv('bb_price.csv', encoding='utf-8', index=False)
    # import pdb
    # pdb.set_trace()
    # master_df = pd.read_excel(
    #     "/home/asarudheen/Downloads/ProductID.xlsx")
    # df = df[df.bb_id.isin([4, 10000755])]
    #  fill null values as 0 and change type to integer
    # master_df['Bigbasket'] = master_df['Bigbasket'].fillna(0).astype(int)
    #  merge F2H and master dataframe to get only matched rows
    # bb_df = df.merge(
    #     master_df,
    #     left_on='bb_id',
    #     right_on='Bigbasket',
    #     how='inner')
    #  convert price per kg
    # df['bb_weight'] = np.where(
    #     df.bb_weight.str.contains('gm'),
    #     df.bb_weight.str.extract('(\d+)').astype(int),
    #     df.bb_weight.str.extract('(\d+)').astype(int) * 1000)
    # df.bb_price = df.bb_price.astype(
    #     float) / df.bb_weight.astype(float) * 1000

    # import pdb
    # pdb.set_trace()

    # return bb_df[["SKU_NAME", "bb_id", "bb_price"]]

    # def final_report(self):
    #     """To get data comparison report.

    #     Returns:
    #         final_report

    #     """
    #     f2h_report = self.from_F2H()
    #     bb_report = self.from_bigbasket()
    #     #  merge F2H and bigbasket reports with outer join
    #     final_df = F2H_report.merge(BB_report, left_on='SKU_NAME', right_on='SKU_NAME', how='outer')[['SKU_NAME', 'f2h_price', 'bb_price']]
    #     final_df = final_df.set_index(['SKU_NAME'])
    #     print (final_df)
    #     file_handles = []
    #     #  create tempfile and attach final csv report
    #     with tempfile.NamedTemporaryFile(mode='r+') as temp:
    #         print (temp.name)
    #         final_df = final_df.to_csv(temp)
    #         temp.seek(0)
    #         file_handles.append(temp.name)
    #         Mail().send("testtendercuts2@gmail.com", "naveen@tendercuts.in", "Price Comparison", "Price comparison", file_handles)

    #     return True


def fipola_price():
    product_url = "https://store.baskmart.com/api/app/products?store_id=59cd293f3d0a06c213f9b98c"
    res = requests.get(product_url)
    fipola_data = res.json()
    # import pdb
    # pdb.set_trace()

    fipola_list = []
    for i in range(len(fipola_data)):
        # import pdb
        # pdb.set_trace()
        for a in fipola_data[i]['products']:
            # import pdb
            # pdb.set_trace()
            try:
                fipola_list.append(
                    (a["_id"],
                     a['category'],
                     a['name'],
                        a['sellingPrice'],
                     a['custom_fields']['Gross'],
                     a['custom_fields']['Net']))
            except KeyError:
                continue

    # import pdb
    # pdb.set_trace()
    #  create dataframe for F2H and master
    df = pd.DataFrame(
        fipola_list,
        columns=[
            "id",
            "category",
            "name",
            "sellingPrice", "Gross", "Net"])
    # import pdb
    # pdb.set_trace()
    return df
    # df.to_csv('fib_price.csv', encoding='utf-8', index=False)
if __name__ == '__main__':
    df = fipola_price()
    print df
    # import pdb
    # pdb.set_trace()
    # df1 = bigbasket_report()
    # df2 = licious_report()
    # df3 = f2h_report()
    # writer = pd.ExcelWriter('product_prices.xlsx', engine='xlsxwriter')
    # pdb.set_trace()
    # df.to_excel(writer, sheet_name='fipola_price')
    # df1.to_excel(writer, sheet_name='big_basket_price')
    # df2.to_excel(writer, sheet_name='licious_price')
    # df3.to_excel(writer, sheet_name='fresh2home_price')
    # print df1
