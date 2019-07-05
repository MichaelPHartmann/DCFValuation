import os
import sys
import random
PATH_TO_API = os.path.abspath("../FinMesh")
sys.path.insert(0, PATH_TO_API)
import iex.stock
from dcf import *

class stock:
    def __init__(self, symbol):
        self.keystats = iex.stock.key_stats(symbol)


class sub:
    def __init__(self,symbol):
        symbol = stock(symbol)
        self.sharesOutstanding = symbol.keystats['sharesOutstanding']

AAPL = sub('AAPL')

print(AAPL.sharesOutstanding)
