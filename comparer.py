
from utils import load_json, save_info_to_json

# Converts the list of product dicts to a dict keyed by the product id.


def index_by_id(collected_product_info):
    by_id = {p["id"]: p for p in collected_product_info}
    return by_id


# Compares the current search results with the previous results and returns a product info dictionary including stock changes
def compare_stocks(current=None, previous=None):
    previous_by_id = index_by_id(previous)
    previous_set_ids = set(previous_by_id)

    current_by_id = (index_by_id(current))
    current_set_ids = set(current_by_id)

    common_ids = current_set_ids & previous_set_ids
    new_ids = current_set_ids - previous_set_ids
    # removed_ids = previous_set_ids - current_set_ids

    print("Common id's with last search:", common_ids)
    print("New id's since last search:", new_ids)
    # print("Removed id's since last search:", removed_ids)

    changed_products_info = {}

    # Helper function to add stock changes
    def add_product_info(product_id, product_data, stock_difference, reason, in_stock):
        changed_products_info[product_id] = product_data.copy()
        changed_products_info[product_id].update({
            'update': reason,
            'stock_difference': stock_difference,
            'in_stock': in_stock
        })

    # Sets the stock difference and change reason e.g. new in stock.
    for id in common_ids:
        before = previous_by_id[id]["stock"]
        after = current_by_id[id]["stock"]
        difference = after-before
        print(
            f"ID: {id}, Before: {before}, after: {after}, difference:{difference}")

        if difference > 0 and before == 0 and after > 0:
            add_product_info(
                id, current_by_id[id], difference, "New In Stock", True)

        elif difference > 0 and before > 0 and after > 0:
            add_product_info(
                id, current_by_id[id], difference, "Stock Added", True)

        elif difference < 0 and after > 0:
            add_product_info(
                id, current_by_id[id], difference, "Stock Lessened", True)

        elif difference == 0 and after > 0:
            add_product_info(
                id, current_by_id[id], difference, "Still In Stock", True)

        elif difference < 0 and after <= 0:
            add_product_info(
                id, current_by_id[id], difference, "Out Of Stock", False)

        elif difference == 0 and after <= 0:
            add_product_info(
                id, current_by_id[id], difference, "Still Out Of Stock", False)
        else:
            add_product_info(
                id, current_by_id[id], difference, "Unknown", False)

    # Add info for those products with id's that were not found before
    for id in new_ids:
        if current_by_id[id]['stock'] > 0:
            add_product_info(
                id, current_by_id[id], current_by_id[id]['stock'], "New Print In Stock", True)

    # for id in removed_ids:
    #     previous_stock = -int(previous_by_id[id]['stock'])
    #     add_product_info(
    #         id, previous_by_id[id], previous_stock, "Print found previously, but seems to have been removed")

    return changed_products_info


###################################################
#  Orchestrator
###################################################

def compare_product_info(collected_product_info, previous_file_path):
    previous = load_json(previous_file_path)
    current = collected_product_info
    compared_product_info = compare_stocks(previous=previous, current=current)
    return compared_product_info


###################################################
####                Main                        ###
###################################################
if __name__ == "__main__":
    from config import PREV_COLLECTED_JSON_PATH

    # Run comparer on mock collected data compared to a previous collected json file
    current = load_json("collected_product_mock.json")
    compared = compare_product_info(current, PREV_COLLECTED_JSON_PATH)
    print(compared)
    save_info_to_json(compared, "compared_product_mock.json")
