class Product:
    def __init__(self, original, name, manufacturer, model, family, announced_date):
        self.original = original
        self.original_name = name
        self.name = name.lower()
        self.manufacturer = manufacturer.lower()
        self.model = model.lower()
        if family is not None:
            self.family = family.lower()
        else:
            self.family = None
        self.announced_date = announced_date.lower()

    def __str__(self):
        return "\nProduct Name: " + repr(self.name) + "\nManufacturer: " + repr(self.manufacturer) + \
               "\nModel: " + repr(self.model) + "\nFamily: " + repr(self.family) + "\nAnnounced Date: " \
               + repr(self.announced_date) + "\n"

    def print_json(self):
        return "{\"product name\":\"" + self.name + "\",\"Manufacturer\":\"" + self.manufacturer + \
               "\",\"model\":\"" + self.model + "\",\"family\":\"" + repr(self.family) + \
               "\",\"announced date\":\"" + self.announced_date + "\"}"

    def __repr__(self):
        return "\nProduct Name: " + repr(self.name) + "\nManufacturer: " + repr(self.manufacturer) + \
               "\nModel: " + repr(self.model) + "\nFamily: " + repr(self.family) + "\nAnnounced Date: " \
               + repr(self.announced_date) + "\n"
