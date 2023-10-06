import time
import unittest
from test.support_functions import start_test_redis, stop_test_redis

from redis.exceptions import ConnectionError

from config import store_params_fail, store_params_ok
from db.store import Store, StoreFake


class TestStoreOK(unittest.TestCase):
    # execute before all tests
    @classmethod
    def setUpClass(cls):
        start_test_redis()
        time.sleep(1)
        print("setUpClass")
        cls.store = StoreFake(store_params=store_params_ok)

    # execute after all tests
    @classmethod
    def tearDownClass(cls):
        stop_test_redis()

    # execute before each tests
    def setUp(self):
        pass

    # execute after each tests
    def tearDown(self):
        keys_all = self.store.r.keys("*")
        if keys_all:
            self.store.r.delete(*keys_all)

    def test_set_ok(self):
        key_set = "foo"
        # key_set = [1,2]
        val_set = "bar"
        self.store.set(key_set, val_set)
        val_get = self.store.r.get(key_set)

        self.assertEqual(val_set, val_get)

    def test_set_cache_ok(self):
        key_set = "foo"
        val_set = "bar"
        expire_time = 1
        self.store.set_cache(key_set, val_set, expire_time)
        val_get = self.store.get(key_set)

        self.assertEqual(val_set, val_get)

        time.sleep(expire_time)
        val_get = self.store.r.get(key_set)

        self.assertEqual(None, val_get)

    def test_get_ok(self):
        key_set = "foo"
        # key_set = [1,2]
        val_set = "bar"
        self.store.r.set(key_set, val_set)
        val_get = self.store.get(key_set)

        self.assertEqual(val_set, val_get)

    def test_get_cache_ok(self):
        key_set = "foo"
        val_set = "bar"
        expire_time = 1
        self.store.r.set(key_set, val_set, expire_time)
        val_get = self.store.get_cache(key_set)

        self.assertEqual(val_set, val_get)

        time.sleep(expire_time)
        val_get = self.store.r.get(key_set)

        self.assertEqual(None, val_get)


class TestStoreFail(unittest.TestCase):
    # execute before all tests
    @classmethod
    def setUpClass(cls):
        print("setUpClass")
        cls.store = Store(store_params=store_params_fail)

    def test_set_fail(self):
        key_set = "foo"
        val_set = "bar"

        with self.assertRaises(ConnectionError):
            self.store.set(key_set, val_set)

    def test_set_cache_fail(self):
        key_set = "foo"
        val_set = "bar"
        expire_time = 100
        val_set = self.store.set_cache(key_set, val_set, expire_time)
        self.assertEqual(None, val_set)

    def test_get_fail(self):
        key_set = "foo"

        with self.assertRaises(ConnectionError):
            self.store.get(key_set)

    def test_get_cache_fail(self):
        key_set = "foo"

        val_get = self.store.get_cache(key_set)
        self.assertEqual(None, val_get)
