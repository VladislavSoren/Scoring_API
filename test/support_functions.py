import functools
import subprocess


def cases(cases):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                new_args = args + (c if isinstance(c, tuple) else (c,))
                f(*new_args)

        return wrapper

    return decorator


def start_test_redis():
    subprocess.run(["docker", "start", "redis_test"])


def stop_test_redis():
    subprocess.run(["docker", "stop", "redis_test"])
