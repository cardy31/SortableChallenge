import json
import re

from fuzzywuzzy import fuzz

from src.Listing import Listing
from src.Product import Product

# The goal is to match as many listings to products as possible


class Matcher:
    def __init__(self):
        # Deal with sorting products by manufacturer
        listings = self.get_listings()
        products = self.get_products()

        # Create a list of all manufacturers
        self.manufacturers = []

        for product in products:
            if product.manufacturer not in self.manufacturers:
                self.manufacturers.append(product.manufacturer)

        # Sort products into a list for each manufacturer
        self.manufacturer_buckets = {}

        # Create a bucket for every manufacturer
        for i in range(0, len(self.manufacturers)):
            self.manufacturer_buckets[self.manufacturers[i]] = []

        # Add each listing to a manufacturer bucket
        for i in range(0, len(listings)):
            for j in range(0, len(self.manufacturers)):
                if self.manufacturers[j] in listings[i].manufacturer:
                    self.manufacturer_buckets[self.manufacturers[j]].append(listings[i])

                elif self.manufacturers[j] in listings[i].title:
                    self.manufacturer_buckets[self.manufacturers[j]].append(listings[i])
                    # print('Man: {}\n{}'.format(self.manufacturers[j], listings[i]))

        print(self.manufacturer_buckets.keys())

        # Create regex patterns to match manufacturers with whitespace in the name. ie. Ca sio
        self.manufacturers_whitespace_regex = []
        for manufacturer in self.manufacturers:
            manufacturer.replace('canada', '')
            # Put a '0 or 1 spaces' regex in between every character in the manufacturer's name
            new_string = manufacturer.replace('', '\s?')[3: -3]
            self.manufacturers_whitespace_regex.append(new_string)

        # for i in range(0, len(listings)):
        #     for man in self.manufacturers_whitespace_regex:
        #         search_obj = re.search(man, listings[i].title, re.IGNORECASE)
        #         if search_obj:
        #             if listings[i] not in self.manufacturer_buckets[man.replace('\\s?', '')]:
        #                 self.manufacturer_buckets[man.replace('\\s?', '')].append(listings[i])

        self.make_matches(products, listings)

    def make_matches(self, products, listings):
        no_manufacturer_match = 0
        manufacturer_found_but_no_prod_match = 0

        limit = 10
        for i in range(2, 3):
            product = products[i]
            manufacturer_found = False

            # Fix manufacturer variation ie "canon canada" becomes "canon", and add manufacturer to likely manufacturers
            for manufacturer in self.manufacturers_whitespace_regex:
                search_obj = re.search(manufacturer, product.manufacturer, re.IGNORECASE)
                if search_obj:
                    product.manufacturer = manufacturer.replace('\\s?', '')
                    manufacturer_found = True
                    break

            if manufacturer_found is False:
                print(product)
                print('Manufacturer does not match\n')
                continue

            five = []
            ten = []
            fifteen = []
            twenty = []

            print(product)
            final = None
            for listing in self.manufacturer_buckets[product.manufacturer]:
                points = 0
                if product.manufacturer in listing.title:
                    points += 5
                if product.family is not None and product.family in listing.title:
                    points += 5
                if product.model in listing.title:
                    # print('{}, {}'.format(product.model, listing.title))
                    points += 10

                if points == 5:
                    five.append(listing)
                elif points == 10:
                    ten.append(listing)
                elif points == 15:
                    fifteen.append(listing)
                elif points == 20:
                    twenty.append(listing)

                curr_low = 1000000000
                final = None

                if len(twenty) == 0:
                    for match in fifteen:
                        if match.manufacturer != product.manufacturer:
                            continue
                        if float(match.price) < curr_low:
                            final = match
                            curr_low = float(match.price)
                else:
                    for match in twenty:
                        if match.manufacturer != product.manufacturer:
                            continue
                        if float(match.price) < curr_low:
                            final = match
                            curr_low = float(match.price)

            print('Five: {}\n'
                  'Ten: {}\n'
                  'Fifteen: {}\n'
                  'Twenty: {}\n'.format(len(five), len(ten), len(fifteen), len(twenty)))

            print(product)
            # print(fifteen)
            print(twenty)
            print(final)


            # likely_matches = []
            curr_max = 0
            best_man = ''
            best_man_index = 0

            # for manufacturer in likely_manufacturers:
            #     for j in range(0, len(self.manufacturer_buckets[manufacturer])):
            #         product = self.manufacturer_buckets[manufacturer][j]
            #         score = fuzz.ratio('{} {}'.format(product.manufacturer, product.model), listing.title)
            #         curr_max = max(score, curr_max)
            #         best_man = manufacturer
            #         best_man_index = j
            #
            # print('Score: {}, Best Manufacturer: {}, Index: {}\n'
            #       'Listing: {}\n'
            #       'Match: {}\n\n'.format(curr_max,
            #                              best_man,
            #                              best_man_index,
            #                              listing,
            #                              self.manufacturer_buckets[best_man][best_man_index]))

    def title_contains_model(self, title, model):
        if title.__contains__(model):
            return True



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
