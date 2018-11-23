import json


class Listing:
    def __init__(self, title, manufacturer, currency, price):
        self.title_original = title
        self.title = title.lower()
        self.manufacturer_original = manufacturer
        self.manufacturer = manufacturer.lower()
        self.currency = currency
        self.price = price

    def __str__(self):
        return "\nTitle: " + repr(self.title) + "\nManufacturer: " + repr(self.manufacturer) + \
               "\nCurrency: " + repr(self.currency) + "\nPrice: " + repr(self.price) + "\n"

    def __repr__(self):
        return "\nTitle: " + repr(self.title) + "\nManufacturer: " + repr(self.manufacturer) + \
               "\nCurrency: " + repr(self.currency) + "\nPrice: " + repr(self.price) + "\n"

    def to_json(self):
        data = {
            'title': self.title_original,
            'manufacturer': self.manufacturer_original,
            'currency': self.currency,
            'price': self.price
        }
        return json.dumps(data)
