import json


class Result:
    def __init__(self, product_name):
        self.product_name = product_name
        self.listings = []

    def to_json(self):
        json_listings = ''
        if len(self.listings) > 0:
            for i in range(0, len(self.listings) - 1):
                listing = self.listings[i]
                json_listings += listing.to_json()
                json_listings += ','

            temp = self.listings[-1].to_json()
            json_listings += temp

        val = '{\n' + '\"product_name\": \"{}\",\n\"listings\": [{}]'.format(self.product_name, json_listings) + '\n}'

        return val

    def __repr__(self):
        return "\nProduct Name: {}\nListings: {}".format(self.product_name, self.listings)

    def __str__(self):
        return self.__repr__()
