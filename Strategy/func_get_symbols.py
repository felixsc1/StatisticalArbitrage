from config_strategy_api import session


def get_tradeable_symbols(rebate=False):
    # Get symbols that are tradeable

    # optional filter out pairs that offer maker rebate
    maker_fee = 0 if rebate else 0.1

    sym_list = []
    symbols = session.query_symbol()  # see pybit documentation
    # filter out result data if request worked.
    if "ret_msg" in symbols.keys():
        if symbols["ret_msg"] == "OK":
            symbols = symbols["result"]

            # if OK, filter symbols according to our strategy
            # Problem as of April 2022, only few symbols have negative maker fee, adjusted it therefore...
            for symbol in symbols:
                if symbol["quote_currency"] == "USDT" and float(symbol["maker_fee"]) < maker_fee and symbol["status"] == "Trading":
                    sym_list.append(symbol)
            return sym_list
