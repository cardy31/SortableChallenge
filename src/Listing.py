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

    def print_json(self):
        return "{\"title\":\"" + self.title + "\",\"Manufacturer\":\"" + self.manufacturer + \
               "\",\"Currency\":\"" + self.currency + "\",\"Price\":\"" + self.price + "\"}"
