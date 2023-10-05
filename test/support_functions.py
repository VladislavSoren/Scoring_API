import functools
import subprocess


def cases(cases):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args):
            for c in cases:
                new_args = args + (c if isinstance(c, tuple) else (c,))
                try:
                    f(*new_args)
                except AssertionError as e:
                    raise AssertionError(f"{e}, args: {c}")

        return wrapper

    return decorator


def start_test_redis():
    subprocess.run(["docker", "start", "redis_test"])


def stop_test_redis():
    subprocess.run(["docker", "stop", "redis_test"])
