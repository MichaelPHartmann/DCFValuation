import os
import sys
PATH_TO_API = os.path.abspath("../FinMesh")
sys.path.insert(0, PATH_TO_API)
import iex.stock
from dcf import *

print(beta('AAPL'))
