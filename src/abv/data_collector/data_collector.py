import os
import time
import logging
import datetime
import requests
from abv.file_location import FileLocation



def write_beer_inventory():
    beer_inventory = get_inventory()
    if beer_inventory != "":
        write_inventory(beer_inventory)


def write_inventory(beer_inventory):
    file_location_object = FileLocation()
    file_location = file_location_object.get_file_location()
    filename = os.path.join(file_location, str(datetime.datetime.now()).replace(' ', '_') + '.csv')

    try:
        with open(filename, "w+") as beer_inventory_file:
            beer_inventory_file.write(beer_inventory)
        logging.info('The data was fetched successfully!')
    except OSError as e:
        error_subclass = type(e).__name__
        logging.exception('Failed to fetch file: {}'.format(error_subclass))


def get_inventory():
    beer_file = 'http://www.tanczos.com/tanczos.com/beerinventory/webexport.csv'
    try:
        beer_inventory = requests.get(beer_file)
        return beer_inventory.text
    except requests.exceptions.ConnectionError as e:
        error_subclass = type(e).__name__
        logging.exception('Failed to fetch file: {}'.format(error_subclass))
        return ""


def run():
    """
    Runs write_beer_inventory every 20 minutes

    Input:
        None

    Output:
        Returns void
    """

    seconds_between_fetches = 1200

    while True:
        write_beer_inventory()
        time.sleep(seconds_between_fetches)


if __name__ == "__main__":
    logging.basicConfig(filename='abv.log', level=logging.INFO, format='%(asctime)s:%(message)s')
    run()
