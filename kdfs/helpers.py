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
