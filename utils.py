import json
from datetime import date


def load_wishlist(file_name="wishlist.txt"):
    with open(file_name, 'r',) as file:
        cards = [line.strip() for line in file if line.strip()]
        return cards


def save_info_to_json(product_info, file_name="unnamed_info.json"):
    with open(file_name, 'w') as file:
        file.write(json.dumps(product_info, indent=2))


def save_info_to_txt(product_info, file_name="unnamed_info.txt"):
    with open(file_name, 'w') as file:
        file.write(json.dumps(product_info))


def load_json(file_name):
    with open(file_name, "r") as file:
        loaded_file = json.load(file)
    return loaded_file


def save_mail_html(message, file_name=f"notification_{date.today()}.html"):
    with open(file_name, "w") as file:
        file.write(message)


# Printing functions for during testing:
def format_stock_info(collected_info):
    lines = []
    for info in collected_info:
        in_stock = "✓" if info["stock"] > 0 else "✗"
        lines.append(
            f"{in_stock} ID:{info['id']:6} {info['name']:30} ({info['set']:4}) - €{info['price']:6} - Stock: {info['stock']}"
        )
    return "\n".join(lines)


def print_stock(collected_products_info):
    for info in collected_products_info:
        in_stock = "✓" if info["stock"] > 0 else "✗"
        print(
            f"{in_stock} ID:{info['id']:6} {info['name']:30} ({info['set']:4}) - €{info['price']:6} - Stock: {info['stock']}"
        )

def print_info(filtered_product_info, selection="undefined"):
    print(f"Card updates for {selection} selection")
    for product in filtered_product_info:
        print(f"Name: {product["name"]}")
        print(f"Price: {product["price"]}")
        print(f"Stock left: {product["stock"]}")

    return
