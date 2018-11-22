import json
import re
# TODO: Remove this before submission
import sys


from fuzzywuzzy import fuzz

from src.Listing import Listing
from src.Product import Product
from src.Result import Result

# The goal is to match as many listings to products as possible


class Matcher:
    def __init__(self):
        # Open a file to write results to
        self.output_file = open('/Users/cardy/Programming/PycharmProjects/SortableChallenge2/json/results.txt', 'w')

        # Read listings and products
        listings = self.get_listings()
        products = self.get_products()

        # Create a list of all product manufacturers
        self.manufacturers = []

        for product in products:
            if product.manufacturer not in self.manufacturers:
                self.manufacturers.append(product.manufacturer)

        # Sort listings into a list for each manufacturer
        self.listings_by_manufacturer = {}

        # Create a bucket for every manufacturer
        for i in range(0, len(self.manufacturers)):
            self.listings_by_manufacturer[self.manufacturers[i]] = []

        # Add each listing to a manufacturer bucket if the manufacturer name is in the title or manufacturer section
        for i in range(0, len(listings)):
            for j in range(0, len(self.manufacturers)):
                if self.manufacturers[j] in listings[i].manufacturer:
                    self.listings_by_manufacturer[self.manufacturers[j]].append(listings[i])

                elif self.manufacturers[j] in listings[i].title:
                    self.listings_by_manufacturer[self.manufacturers[j]].append(listings[i])

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

        self.make_matches(products, listings)

    def make_matches(self, products, listings):
        # Counters
        no_manufacturer_match = 0

        results = {}
        for product in products:
            results[product.original_name] = Result(product.original_name)

        for i in range(0, len(listings)):
            if i > 100 and i % 100 == 0:
                print('Finished {} listings'.format(i))
            listing = listings[i]
            manufacturer_found = False
            likely_manufacturers = []

            # Fix manufacturer variation ie "canon canada" becomes "canon", and add manufacturer to likely manufacturers
            for manufacturer in self.manufacturers_whitespace_regex:
                search_obj = re.search(manufacturer, '{}{}'.format(listing.manufacturer, listing.title), re.IGNORECASE)
                if search_obj:
                    likely_manufacturers.append(manufacturer.replace('\\s?', ''))
                    manufacturer_found = True
                    # print('Added to {}'.format(listing.manufacturer))

            if manufacturer_found is False:
                # print('Manufacturer does not match: {}\n'.format(listing))
                no_manufacturer_match += 1
                continue

            five = []
            ten = []
            fifteen = []

            final = None

            for manufacturer in likely_manufacturers:
                # print(manufacturer)
                for product in self.products_by_manufacturer[manufacturer]:
                    points = 0
                    if listing.manufacturer in product.manufacturer or product.manufacturer in listing.manufacturer:
                        # print('Manufacturer match')
                        points += 5
                    if self.title_contains_model(product.model, listing.title):
                        points += 5
                    if product.family is not None and product.family in listing.title:
                        # print('Family match')
                        points += 5
                    elif product.family is None:
                        points += 5

                    if points == 10:
                        ten.append(product)
                    if points == 15:
                        fifteen.append(product)

            # print('Listing: {}'.format(listing))
            # print('Fifteen: {}'.format(fifteen))

            if fifteen is not None:
                for product in fifteen:
                    results[product.original_name].listings.append(listing)
                    # print(results[product.original_name].to_json())

        for result in results.values():
            if result.listings is not None:
                self.output_file.write(result.to_json())

        print('No manufacturer match:', no_manufacturer_match)


    @staticmethod
    def title_contains_model(model, title):
        model = model.replace('-', '')
        model = model.replace(' ', '')
        model = model.replace('_', '')
        regex_model = model.replace('', '[-\ _]?')
        search_obj = re.search(regex_model, title, re.IGNORECASE)
        if search_obj:
            return True
        return False

    @staticmethod
    def get_listings():
        # Create an object for each listing
        listing_json_entries = []
        for line in open('../json/listings.txt', 'r'):
            listing_json_entries.append(json.loads(line))
        listings = []

        for i in range(0, listing_json_entries.__len__()):
            title = listing_json_entries[i]['title'].lower()
            manufacturer = listing_json_entries[i]['manufacturer'].lower()
            currency = listing_json_entries[i]['currency'].lower()
            price = listing_json_entries[i]['price'].lower()
            new_listing = Listing(listing_json_entries[i], title, manufacturer, currency, price)
            listings.append(new_listing)

        print("Number of Listings: {}".format(listings.__len__()))
        return listings

    @staticmethod
    def get_products():
        # Create an object for each product
        product_json_entries = []
        for line in open('../json/products.txt', 'r'):
            product_json_entries.append(json.loads(line))
        products = []

        for i in range(0, product_json_entries.__len__()):
            product_name = product_json_entries[i]['product_name'].lower()
            manufacturer = product_json_entries[i]['manufacturer'].lower()
            model = product_json_entries[i]['model'].lower()
            try:
                family = product_json_entries[i]['family'].lower()
            except KeyError:
                family = None
            announced_date = product_json_entries[i]['announced-date'].lower()
            new_product = Product(product_json_entries[i], product_name, manufacturer, model, family, announced_date)
            products.append(new_product)

        print("Number of Products: " + repr(products.__len__()))
        return products


class ListScores:
    def __init__(self, listing, score):
        self.listing = listing
        self.score = score


if __name__ == '__main__':
    match = Matcher()
