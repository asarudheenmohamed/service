class SalesOrder:
    def __init__(self, data, shipping_address):
        self.__data = data
        self.shipping_address = shipping_address

        # should be populated automatically
        self.map_point = None

    @property
    def order_id(self):
        return self.__data['order_id']
