import json
import re
import sys

from Listing import Listing
from Product import Product
from Result import Result

# Paths to JSON files
LISTING_JSON = '../json/listings.txt'
PRODUCT_JSON = '../json/products.txt'
OUTPUT_FILE = '../json/results.txt'


class Matcher:
    def __init__(self):
        print('Performing initial value parse')
        # Open a file to write results to
        try:
            self.output_file = open(OUTPUT_FILE, 'w')
        except FileNotFoundError:
            print('If you could make sure that that the paths at the top'
                  ' of Main.py are valid then that would be great!')
            print('Have a nice day! :)')
            sys.exit()

        # Read listings and products
        products = self.get_products()

        # Create a list of all product manufacturers
        self.manufacturers = []

        for product in products:
            if product.manufacturer not in self.manufacturers:
                self.manufacturers.append(product.manufacturer)

        # Sort products into a dict where every key is a manufacturer's name, every value is an array containing
        # all product made by that manufacturer
        self.products_by_manufacturer = {}

        for product in products:
            if product.manufacturer not in self.products_by_manufacturer.keys():
                self.products_by_manufacturer[product.manufacturer] = []
                self.products_by_manufacturer[product.manufacturer].append(product)
            else:
                self.products_by_manufacturer[product.manufacturer].append(product)

        # Create regex patterns to match manufacturers with whitespace in the name. ie. Ca sio
        self.manufacturers_whitespace_regex = []
        for manufacturer in self.manufacturers:
            # Put a '0 or 1 spaces' regex in between every character in the manufacturer's name
            new_string = manufacturer.replace('', '\s?')[3: -3]
            self.manufacturers_whitespace_regex.append(new_string)

        self.make_matches(products)

    def make_matches(self, products):
        # Result object are stored in here to provide O(1) access for storing listings matching a product
        results = {}

        for product in products:
            results[product.original_name] = Result(product.original_name)

        # Counter to update user on progress
        count = 0

        listings_file_pointer = self.get_listings_file_pointer()

        print('Generating matches')
        for line in listings_file_pointer:
            # Get the current listing
            listing = self.create_listing(line)

            # Give user updates on completion
            if count > 300 and count % 300 == 0:
                val = int((count / 20196) * 100)
                print('{}% Complete'.format(val))

            # Narrow down products by checking for manufacturer names in the listing's manufacturer and title fields
            likely_manufacturers = self.find_likely_manufacturers(listing)

            # If there aren't any likely manufacturers then we move onto the next listing
            if len(likely_manufacturers) == 0:
                continue

            for manufacturer in likely_manufacturers:
                found = False
                for product in self.products_by_manufacturer[manufacturer]:
                    if self.product_matches_listing(product, listing):
                        found = True
                        results[product.original_name].listings.append(listing)
                        break
                # If we've already found a match for a listing, we move onto the next listing
                if found:
                    break

            count += 1

        # Write results out to file
        for result in results.values():
            if result.listings is not None:
                self.output_file.write(result.to_json())

        print('100% Complete')
        print('\nCheck [project_directory]/json/results.txt for the results!')

    def find_likely_manufacturers(self, listing):
        """
        Checks a listing object's title and manufacturer fields to see what, if any, manufacturer names are in them
        :param listing: A listing object
        :return: List of manufacturers as strings
        """
        likely_manufacturers = []
        for manufacturer in self.manufacturers_whitespace_regex:
            search_obj = re.search(manufacturer, '{}{}'.format(listing.manufacturer, listing.title), re.IGNORECASE)
            if search_obj:
                likely_manufacturers.append(manufacturer.replace('\\s?', ''))
        return likely_manufacturers

    def product_matches_listing(self, product, listing):
        """
        This method is just a lot of if statements that check for various string/regex matches in the listing
        :param product: Product object
        :param listing: Listing object
        :return: Boolean
        """
        # Manufacturer check
        if listing.manufacturer in product.manufacturer or product.manufacturer in listing.manufacturer:
            # Model check
            if self.substring_in_string_with_allowances(product.model, listing.title):
                # Family check
                if product.family is None or self.substring_in_string_with_allowances(product.family,
                                                                                      listing.title):
                    return True
        return False

    @staticmethod
    def substring_in_string_with_allowances(substring, string):
        """
        Uses a regex to check if the substring is in the string. Allows for a few characters mixed in.
        For example, a substring of s5000 will match to 's 5000', 's_5000', 's-5-000', etc.
        :param substring: The model code to look for in the title.
        :param string: The title to search for the model code.
        :return:
        """
        substring = substring.replace('-', '')
        substring = substring.replace(' ', '')
        substring = substring.replace('_', '')
        regex_model = substring.replace('', '[-\ _]?')
        regex_model = regex_model[7:-7]
        regex_model = '[^A-z,^0-9]' + regex_model + '(hd)?[^A-z,^0-9]'
        search_obj = re.search(regex_model, string, re.IGNORECASE)
        if search_obj:
            return True
        return False

    @staticmethod
    def get_listings_file_pointer():
        try:
            fp = open(LISTING_JSON, 'r')
        except FileNotFoundError:
            print('If you could make sure that that the paths at the top'
                  ' of Main.py are valid then that would be great!')
            print('Have a nice day! :)')
            sys.exit()
        return fp

    @staticmethod
    def create_listing(listing_json):
        """
        :param listing_json: The raw json object for one listing
        :return: A new Listing object
        """
        # Convert json to dict
        dict_from_json = json.loads(listing_json)

        # Parameters for Listing object creation
        title = dict_from_json['title']
        manufacturer = dict_from_json['manufacturer']
        currency = dict_from_json['currency']
        price = dict_from_json['price']

        return Listing(title, manufacturer, currency, price)

    def get_products(self):
        """
        :return: A list of Product objects, one object per JSON product
        """
        products = []
        try:
            for line in open(PRODUCT_JSON, 'r'):
                products.append(self.create_product(line))
        except FileNotFoundError:
            print('If you could make sure that that the paths at the top'
                  ' of Main.py are valid then that would be great!')
            print('Have a nice day! :)')
            sys.exit()

        return products

    @staticmethod
    def create_product(product_json):
        """
        :param product_json: The raw JSON object for one product
        :return: A new Product object
        """
        # Convert json to dict
        dict_from_json = json.loads(product_json)

        # Parameters for Product object creation
        product_name = dict_from_json['product_name']
        manufacturer = dict_from_json['manufacturer']
        model = dict_from_json['model']
        try:
            family = dict_from_json['family']
        except KeyError:
            family = None
        announced_date = dict_from_json['announced-date']

        return Product(product_name, manufacturer, model, family, announced_date)


if __name__ == '__main__':
    match = Matcher()
