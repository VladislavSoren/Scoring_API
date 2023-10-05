import redis
from redis.backoff import ExponentialBackoff
from redis.exceptions import ConnectionError  # BusyLoadingError,; TimeoutError
from redis.retry import Retry

# from redis.client import Redis


class Store:
    n_retries = 100
    retry = Retry(ExponentialBackoff(), n_retries)

    def __init__(self, store_params):
        self.r = redis.Redis(
            # В рамках данной реализации переподключение очевидно не работает...
            **store_params,
            retry=self.retry,
            socket_timeout=5,
            retry_on_timeout=True,
            # retry_on_error=[BusyLoadingError, ConnectionError, TimeoutError]
        )
        try:
            self.r.ping()
        except ConnectionError as e:
            print(e)
        else:
            print("Connection is established")
        pass

    def set(self, key, value):
        try:
            self.r.set(key, value)
        except ConnectionError:
            raise ConnectionError

    def set_cache(self, key, value, expire_time):
        try:
            # ms mode (px) work like ex!
            self.r.set(key, value, ex=expire_time)
        except ConnectionError:
            return None

    def get(self, key):
        try:
            return self.r.get(key)
        except ConnectionError:
            raise ConnectionError

    def get_cache(self, key):
        try:
            return self.r.get(key)
        except ConnectionError:
            return None

    def delete(self, key):
        self.r.delete(key)


if __name__ == "__main__":
    store_params = {
        "host": "127.0.0.1",
        # 'port': 6379,
        "port": 6380,
        "db": 0,
        "decode_responses": True,
    }

    store = Store(store_params=store_params)

    store.set("foo", "bar")
    val = store.get("foo")
    print(val)
    print(store.r.keys("*"))
    store.delete("foo")
    print(store.r.keys("*"))
    val = store.get("foo")
    print(val)

    store.set_cache("foo", "bar", 10)
