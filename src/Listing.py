import json

class Listing:
    def __init__(self, original, title, manufacturer, currency, price):
        self.original = original
        self.title = title
        self.manufacturer = manufacturer
        self.currency = currency
        self.price = price

    def __str__(self):
        return "\nTitle: " + repr(self.title) + "\nManufacturer: " + repr(self.manufacturer) + \
               "\nCurrency: " + repr(self.currency) + "\nPrice: " + repr(self.price) + "\n"

    def __repr__(self):
        return "\nTitle: " + repr(self.title) + "\nManufacturer: " + repr(self.manufacturer) + \
               "\nCurrency: " + repr(self.currency) + "\nPrice: " + repr(self.price) + "\n"

    def to_json(self):
        data = {'title': self.title,
                'manufacturer': self.manufacturer,
                'currency': self.currency,
                'price': self.price}

        return '{\n' + '\"title\": \"{}\",\n' \
                       '\"manufacturer\": \"{}\",\n' \
                       '\"currency\": \"{}\",\n' \
                       '\"price\": \"{}\"'.format(self.title,
                                                  self.manufacturer,
                                                  self.currency,
                                                  self.price)\
               + '\n}'
