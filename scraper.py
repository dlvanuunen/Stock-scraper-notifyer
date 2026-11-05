# Scrapes a certain tcg website for products and returns a list of product information dictionaries
import requests
from bs4 import (BeautifulSoup,)
import re

from urllib.parse import unquote

import time

from utils import save_info_to_json
from config import SEARCH_URL, PRODUCT_INFO_URL, USER_AGENT, API_SLEEP, PRODUCTS_TEST, PREV_COLLECTED_JSON_PATH


###################################################
# Search products by name and get product ids
###################################################

# Request the search response of a card
def fetch_search_response(card_name):
    time.sleep(API_SLEEP)
    data = {"queryString": card_name}
    headers = {"User-Agent": USER_AGENT, }

    response = requests.post(
        SEARCH_URL,
        data=data,
        headers=headers,)
    # print("full response card search:\n", response.text,)
    return response


# Extract the weshops product id's from the searched card response
def extract_product_ids(response):
    # Setup html parser and regex pattern
    soup = BeautifulSoup(response.text, "html.parser",)
    id_pattern = re.compile(r"open_product\('(\d+)'\)")
    product_ids = []

    # Extract product IDs from onclick handlers
    for element in soup.find_all(onclick=True):
        line = element["onclick"]
        # print("line:", line,)
        match = re.search(id_pattern, line,)
        if match:
            # print(match.group(1))
            product_ids.append(match.group(1))

    return product_ids


### Product id's search orchestrator ###
def get_product_ids(card_name):
    response = fetch_search_response(card_name)
    product_ids = extract_product_ids(response)
    return product_ids


###################################################
#  Get product information using product_ids
###################################################

# Request the product info of a product id
def fetch_product_info_response(product_id):
    time.sleep(API_SLEEP)
    url = PRODUCT_INFO_URL+product_id
    headers = {
        "User-Agent": USER_AGENT, }
    response = requests.get(url, headers=headers,)
    return response


# Use regex to extract product info from the response
def extract_product_info(response, product_id):
    # print(
    #     f"full response search by product id: {product_id}\n", response.text,)
    # More flexible   r'product_info_\d+.*?value="([^"]+)"',
    # Extract data
    name_match = re.search(
        rf'product_name_{product_id}" value="([^"]+)"', response.text,)

    stock_match = re.search(
        rf'product_stock_{product_id}" value="(\d+)"', response.text,)

    set_match = re.search(
        rf'product_set_{product_id}" value="([^"]+)"', response.text,)

    price_match = re.search(
        rf'product_price_incl_{product_id}" value="([^"]+)"', response.text,)

    img_match = re.search(r'thumb\.php\?src=([^&"]+)', response.text)
    img_url = unquote(img_match.group(1)) if img_match else "?"

    return {
        "id": product_id,
        "name": name_match.group(1) if name_match else "Unknown",
        "stock": int(stock_match.group(1)) if stock_match else 0,
        "set": set_match.group(1) if set_match else "?",
        "price": price_match.group(1) if price_match else "?",
        "img": img_url
    }


### Product info orchestrator ###
def get_product_info(product_id):
    response = fetch_product_info_response(product_id)
    product_info = extract_product_info(response, product_id)
    return product_info


###################################################
#  Scraper orchestrator
###################################################

def collect_products_info(cards_interested):

    ids_by_search_term = {}
    for card_name in cards_interested:

        print(f"Searching for '{card_name}'...\n")
        product_ids = get_product_ids(card_name)
        print(f"Found {len(product_ids)} prints\n")
        ids_by_search_term[card_name] = product_ids

        #     print(f"Found {len(product_ids)} prints\n")
    collected_products_info = []
    for card_name, product_ids in ids_by_search_term.items():
        for product_id in product_ids:
            info = get_product_info(product_id)
            info['search_term'] = card_name
            collected_products_info.append(info)
    return collected_products_info


###################################################
#  Utility functions
###################################################


def print_img_urls(collected_products_info):
    for info in collected_products_info:
        print(info['img'])


 # Test
if __name__ == "__main__":
    print("# Test 1, single card")
    products = collect_products_info(PRODUCTS_TEST)
    print("# Test 1, collected products info: \n")
    print(products)
    print("# Test 1, saving collected products info... \n")
    save_info_to_json(products, PREV_COLLECTED_JSON_PATH)

    # print("# Test 1, print stock info: \n")
    # print_stock(products)
    # print_img_urls(products)

    # print("# Test 2, CARDS_TEST")
    # test_cards = CARDS_TEST
    # products = collect_products_info(test_cards)
    # print("# Test 2, collected products info: \n")
    # print(products)

    # print("# Test 2, print stock info: \n")
    # print(print_stock(products))
