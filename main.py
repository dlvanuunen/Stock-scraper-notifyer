from scraper import collect_products_info
from comparer import compare_product_info
from composer import filter_by_multiple, render_jinja
from mailer import send_mail
from utils import save_info_to_json, load_json, save_mail_html

from config import PRODUCTS_INTERESTED, PREV_COLLECTED_JSON_PATH, COMPARED_JSON_PATH, UPDATE_DAY

from datetime import date



# Test with previously saved compared data
def test_mail_formatting():

    try:
        compared_product_info = load_json(COMPARED_JSON_PATH)

        new = filter_by_multiple(compared_product_info, update=["New In Stock", "New Print In Stock"])
        still_in_stock = filter_by_multiple(compared_product_info, update=["Still In Stock", "Stock Lessened", "Stock Added"])

        message = render_jinja(new, still_in_stock)
        save_mail_html(message)
        send_mail(message)

    except Exception as Err:
        print("An error has occured:", Err)


def main():

    try:
        collected_products_info = collect_products_info(PRODUCTS_INTERESTED)
        compared_product_info = compare_product_info(
            collected_products_info, PREV_COLLECTED_JSON_PATH)
        save_info_to_json(compared_product_info, COMPARED_JSON_PATH)

        # compared_product_info = load_json(COMPARED_JSON_PATH)

        new = filter_by_multiple(compared_product_info, update=[
            "New In Stock", "New Print In Stock"])

        still_in_stock = filter_by_multiple(compared_product_info, update=[
                                            "Still In Stock", "Stock Lessened", "Stock Added"])

        if new or date.today().strftime("%A") == UPDATE_DAY or date.today().strftime("%A") == "Monday":
            print("Time for a new stock update, composing email...")
            message = render_jinja(new, still_in_stock)
            send_mail(message)
        save_info_to_json(collected_products_info, PREV_COLLECTED_JSON_PATH)

    except Exception as Err:
        print("An error has occured:", Err)


if __name__ == "__main__":
    # test_mail_formatting()
    main()
    exit()
