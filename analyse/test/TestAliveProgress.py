import threading

from alive_progress import alive_bar
import time

semaphore = threading.Semaphore(6)

def test_fun():
    with alive_bar(100, ctrl_c=False, title=f'下载{threading.currentThread().name}') as bar:
        for i in range(100):
            time.sleep(0.02)
            print(f"test_fun work: currentThread {threading.currentThread().name}")
            bar()

def test():
    threads = []
    with semaphore:
        for i in range(10):
            thread = threading.Thread(target=test_fun)
            threads.append(thread)
            thread.start()

    print("main_thread 1")
    for thread in threads:
        thread.join()
    print("main_thread 2")

test()
