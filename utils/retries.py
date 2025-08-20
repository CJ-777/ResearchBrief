import time
from functools import wraps


def retry(max_retries: int = 3, delay: float = 2.0):
    """
    Decorator to retry a function on exception.

    Args:
        max_retries (int): Maximum number of retries before raising exception.
        delay (float): Delay in seconds between retries.
    """

    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_retries:
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts >= max_retries:
                        raise
                    print(
                        f"Retry {attempts}/{max_retries} for {fn.__name__} due to: {e}"
                    )
                    time.sleep(delay)

        return wrapper

    return decorator
