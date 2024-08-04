import time
from functools import wraps


def cache_with_ttl(ttl, key_func):  # noqa CFQ004
    def decorator(func):
        cache = {}

        @wraps(func)
        async def wrapped(*args, **kwargs):
            key = key_func(*args, **kwargs)
            current_time = time.time()

            if previous_result := cache.get(key):
                value, timestamp = previous_result
                if current_time - timestamp < ttl:
                    return value

            result = await func(*args, **kwargs)
            cache[key] = (result, current_time)
            return result

        return wrapped
    return decorator
