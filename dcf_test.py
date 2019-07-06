import os
import sys
PATH_TO_API = os.path.abspath("../FinMesh")
sys.path.insert(0, PATH_TO_API)
import iex.stock
import usgov.yieldcurve
import classes
import common

trial = iex.stock.key_stats('AAPL')

for key in trial:
    newkey = 'self.' + key
    print(newkey)
