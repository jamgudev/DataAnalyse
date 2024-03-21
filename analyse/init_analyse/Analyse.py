import time

from analyse.init_analyse.ParseActiveData import mutil_process_iter_files, single_process_iter_files
from analyse.util.FilePathDefinition import TEST_INPUT_FILE, INPUT_FILE
from util import JLog

if __name__ == '__main__':
    startTime = time.time()
    # 可调整并发线程数
    mutil_process_iter_files(INPUT_FILE, 6)
    # single_process_iter_files(INPUT_FILE)
    cost = time.time() - startTime
    JLog.d("Root", f"program takes {cost} s.")
