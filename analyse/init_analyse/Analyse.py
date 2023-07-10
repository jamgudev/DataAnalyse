import time

from analyse.init_analyse.ParseActiveData import mutil_process_iter_files
from analyse.util.FilePathDefinition import TEST_INPUT_FILE
from util import JLog

if __name__ == '__main__':
    startTime = time.time()
    mutil_process_iter_files(TEST_INPUT_FILE, 6)
    cost = time.time() - startTime
    JLog.d("Root", f"program takes {cost} s.")
