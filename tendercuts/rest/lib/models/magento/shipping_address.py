class ShippingAddress():
    def __init__(self, data):
        self.__data = data

    @property
    def street(self):
        return self.__data['street']

    @property
    def city(self):
        return self.__data['city']

    @property
    def postcode(self):
        return self.__data['postcode']

    def to_address(self):
        return "{}, {}, {}".format(self.street, self.city, self.postcode)