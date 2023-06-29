from concurrent.futures import ThreadPoolExecutor


class ThreadPool:
    def __int__(self, maxWorkers: int):
        self.pool = ThreadPoolExecutor(max_workers=maxWorkers, thread_name_prefix="ThreadPool")

    def submit(self, fn, /, *args, **kwargs):
        return self.pool.submit(fn, args, kwargs)

    def shutdown(self, wait=True, *, cancel_futures=False):
        self.pool.shutdown(wait, cancel_futures=cancel_futures)
