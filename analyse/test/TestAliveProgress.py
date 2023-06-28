
from alive_progress import alive_bar
import time

with alive_bar(100, ctrl_c=False, title=f'下载') as bar:
    for i in range(100):
        time.sleep(0.02)
        bar()
