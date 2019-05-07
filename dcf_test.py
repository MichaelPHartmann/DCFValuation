import os
import sys
import random
PATH_TO_API = os.path.abspath("../FinMesh")
sys.path.insert(0, PATH_TO_API)
import iex.stock
from dcf import *



#print(iex.stock.company('AAPL'))

print(beta('AAPL', period='1m', method='averageReg'))
