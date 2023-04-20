import datetime
import functools
import time


def async_exec_time_decorator(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = await func(*args, **kwargs)
        end_time = time.monotonic()
        print(f"Время выполнения асинхронной функции {func.__name__}: {end_time - start_time:.6f} сек.")
        return result

    return wrapper


def exec_time_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        print(f"Время выполнения функции {func.__name__}: {end_time - start_time:.6f} сек.")
        return result

    return wrapper
