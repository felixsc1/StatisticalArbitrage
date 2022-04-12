import pandas as pd
from func_get_symbols import get_tradeable_symbols

"""STRATEGY CODE"""
if __name__ == "__main__":

    # STEP 1 - Get list of symbols
    sym_response = get_tradeable_symbols()
