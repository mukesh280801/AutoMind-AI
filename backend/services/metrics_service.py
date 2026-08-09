import time


class Timer:

    def __init__(self):
        self.start_time = time.perf_counter()

    def elapsed_ms(self):
        """
        Return elapsed time in milliseconds.
        """
        return round((time.perf_counter() - self.start_time) * 1000, 2)