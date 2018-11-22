class Product:
    def __init__(self, original, product_name, manufacturer, model, family, announced_date):
        self.original = original
        self.product_name = product_name.lower()
        self.manufacturer = manufacturer.lower()
        self.model = model.lower()
        if family is not None:
            self.family = family.lower()
        else:
            self.family = None
        self.announced_date = announced_date.lower()

    def __str__(self):
        return "\nProduct Name: " + repr(self.product_name) + "\nManufacturer: " + repr(self.manufacturer) + \
               "\nModel: " + repr(self.model) + "\nFamily: " + repr(self.family) + "\nAnnounced Date: " \
               + repr(self.announced_date) + "\n"

    def print_json(self):
        return "{\"product name\":\"" + self.product_name + "\",\"Manufacturer\":\"" + self.manufacturer + \
               "\",\"model\":\"" + self.model + "\",\"family\":\"" + repr(self.family) + \
               "\",\"announced date\":\"" + self.announced_date + "\"}"

    def __repr__(self):
        return "\nProduct Name: " + repr(self.product_name) + "\nManufacturer: " + repr(self.manufacturer) + \
               "\nModel: " + repr(self.model) + "\nFamily: " + repr(self.family) + "\nAnnounced Date: " \
               + repr(self.announced_date) + "\n"
