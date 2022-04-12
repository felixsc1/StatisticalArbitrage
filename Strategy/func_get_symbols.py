from config_strategy_api import session


def get_tradeable_symbols():
    # Get symbols that are tradeable

    sym_list = []
    symbols = session.query_symbol()  # see pybit documentation
    # filter out result data if request worked.
    if "ret_msg" in symbols.keys():
        if symbols["ret_msg"] == "OK":
            symbols = symbols["result"]
    # filter symbols according to our strategy
    for symbol in symbols:
        if symbol["quote_currency"] == "USDT" and float(symbol["maker_fee"]) < 0 and symbol["status"] == "Trading":
            sym_list.append(symbol)
    print(sym_list)
