import time

from analyse.ParseActiveData import ACTIVE_ROOT_PATH, iter_files
from util import JLog

startTime = time.time()
iter_files(ACTIVE_ROOT_PATH)
cost = time.time() - startTime
JLog.d("Root", f"program takes {cost} s.")
