import os
from dotenv import load_dotenv
from utils import load_wishlist
load_dotenv()


### General ###
PREV_COLLECTED_JSON_PATH = "collected_info.json"
COMPARED_JSON_PATH = "compared_info.json"
UPDATE_DAY = "Friday"


### SCRAPER ###
BASE_URL = os.getenv("BASE_URL")
SEARCH_ENDPOINT = "/inc/public_productsearch.php"
SEARCH_URL = BASE_URL + "/inc/public_productsearch.php"
PRODUCT_INFO_URL = BASE_URL + "/load/product/"
USER_AGENT = os.getenv("USER_AGENT")
# To prevent time-outs
API_SLEEP = 2

PRODUCTS_INTERESTED = load_wishlist("wishlist.txt")
PRODUCTS_TEST= ["Lightning bolt"]


### EMAIL ####
RECIPIENT = os.getenv("RECIPIENT")
SHOP_NAME = os.getenv("SHOP_NAME")
SUBJECT = f"{SHOP_NAME or "Shop X"} stock update!" 

PROVIDER = os.getenv("MY_PROVIDER")

PROVIDER_SETTINGS = {
    "eclipso": {
        "host": "mail.eclipso.de",
        "port": 465,
        "email": os.getenv("ECLIPSO_EMAIL"),
        "password": os.getenv("ECLIPSO_PASSWORD"),
    },
    "skyen": {
        "host": "mail.skyen.live",
        "port": 465,
        "email": os.getenv("SKYEN_EMAIL"),
        "password": os.getenv("SKYEN_PASSWORD"),
    },
    "gmail": {
    "host": "smtp.gmail.com",
    "port": 587,
    "email": os.getenv("GOOGLE_EMAIL"),
    "password": os.getenv("GOOGLE_APP_PASSWORD"),
},
        "my_provider": {
        "host": "mail.your-prodivder.ccTLD",
        "port": 000,
        "email": os.getenv("MY_PROVIDER_EMAIL"),
        "password": os.getenv("MY_PROVIDER_PASSWORD"),
    },
}

active = PROVIDER_SETTINGS[PROVIDER]
SMTP_HOST = active["host"]
SMTP_PORT = active["port"]
EMAIL_ADDRESS = active["email"]
PASSWORD = active["password"]
