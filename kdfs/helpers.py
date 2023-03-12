import functools

from urllib.request import urlopen
import asyncio


# https://stackoverflow.com/questions/41063331/how-to-use-asyncio-with-existing-blocking-library/53719009#53719009
def run_in_executor(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, lambda: f(*args, **kwargs))

    return inner


import time

def count_event_rate(event_count, last_event_time, print_rate=True, units=60):
    current_time = time.time()
    elapsed_time = current_time - last_event_time
    if print_rate and elapsed_time >= units:
        events_per_second = int(event_count / elapsed_time)
        events_per_unit = events_per_second * units
        print(f"Rate per unit: {events_per_unit}")
        event_count = 0
        last_event_time = current_time
    return event_count, last_event_time
