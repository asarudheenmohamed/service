from rest.lib.data_source import prod
import logging


def test_address_fetch():
    FORMAT = 'TEST %(message)s'
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel(logging.DEBUG)
    source = prod.TenderCuts()
    orders =  source.fetch()

    print (orders)
