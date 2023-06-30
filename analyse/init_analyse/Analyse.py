import time

from analyse.init_analyse.ParseActiveData import iter_files
from analyse.util.FilePathDefinition import ACTIVE_ROOT_PATH
from util import JLog

startTime = time.time()
iter_files(ACTIVE_ROOT_PATH)
cost = time.time() - startTime
JLog.d("Root", f"program takes {cost} s.")
