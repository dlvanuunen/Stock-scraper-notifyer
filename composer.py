from utils import load_json, save_mail_html
from jinja2 import Environment, FileSystemLoader
from datetime import date
from config import SHOP_NAME



# Converts product info dict back to a list for filtering
def back_to_list(compared_product_info):
    updated_product_info = [id for id in compared_product_info.values()]
    return updated_product_info


def filter_by_multiple(compared_product_info, operator="and", **filters):
    compared_product_info_list = back_to_list(compared_product_info)

    if operator == "and":
        filtered = compared_product_info_list
        for key, value in filters.items():
            if isinstance(value, list):
                filtered = [
                    product for product in filtered if product.get(key) in value]

            else:
                filtered = [
                    product for product in filtered if product.get(key) == value]
        return filtered

    if operator == "or":
        filtered = []
        for key, value in filters.items():
            if isinstance(value, list):
                matches = [
                    product for product in compared_product_info_list if product.get(key) in value]

            else:
                matches = [
                    product for product in compared_product_info_list if product.get(key) == value]
            filtered.extend(matches)
        return filtered

    else:
        print("unsupperted operator type")



def render_jinja(new, still_in_stock):
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template("notification_template.html")

    message = template.render(
        new=new,
        still_in_stock=still_in_stock,
        date=date.today(),
        shop_name=SHOP_NAME

    )
    return message


if __name__ == "__main__":

    from config import COMPARED_JSON_PATH

    # For testing: load up a previous compared data
    compared_product_info = load_json(COMPARED_JSON_PATH)

    # Filter by new in stock and new prints in stock (prints that were previously not found by the scraper, but are in stock now)
    new = filter_by_multiple(compared_product_info, update=[
                             "New In Stock", "New Print In Stock"])
    # Filter by update reasons with still in stock, stock lessened or stock added.
    still_in_stock = filter_by_multiple(compared_product_info, update=[
                                        "Still In Stock", "Stock Lessened", "Stock Added"])

    save_mail_html(render_jinja(new, still_in_stock))



