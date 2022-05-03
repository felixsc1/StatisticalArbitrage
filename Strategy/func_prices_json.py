from func_price_klines import get_price_klines
import json


def store_price_history(symbols):
    # Store price history for all available pairs

    # Get prices and store in dataframe
    counts = 0
    price_history_dict = {}
    for sym in symbols:
        symbol_name = sym["name"]
        price_history = get_price_klines(symbol_name)
        if len(price_history) > 0:
            price_history_dict[symbol_name] = price_history
            counts += 1
            print(f"{counts} items stored")
        else:
            print(f"item {counts} not stored")
            counts -= 1

    # Store prices as JSON
    if len(price_history_dict) > 0:
        with open("1_price_list.json", "w") as fp:
            json.dump(price_history_dict, fp, indent=4)
        print("prices saved successfully.")

    return
