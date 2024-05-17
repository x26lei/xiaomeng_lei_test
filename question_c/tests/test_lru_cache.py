import unittest
import time
from geo_distributed_cache.cache import LRUCache

class TestLRUCache(unittest.TestCase):
    def setUp(self):
        self.cache = LRUCache(capacity=2, ttl=60)

    def test_set_and_get(self):
        self.cache.set("foo", "bar")
        self.assertEqual(self.cache.get("foo"), "bar")

    def test_lru_eviction(self):
        self.cache.set("a", "1")
        self.cache.set("b", "2")
        self.cache.set("c", "3")  # This should evict "a"
        self.assertIsNone(self.cache.get("a"))
        self.assertEqual(self.cache.get("b"), "2")
        self.assertEqual(self.cache.get("c"), "3")

    def test_ttl_expiry(self):
        self.cache.ttl = 1  # Set TTL to 1 second for testing
        self.cache.set("foo", "bar")
        time.sleep(2)
        self.assertIsNone(self.cache.get("foo"))

    def test_cleanup(self):
        self.cache.ttl = 1
        self.cache.set("foo", "bar")
        self.cache.set("baz", "qux")
        time.sleep(2)
        self.cache._cleanup()
        self.assertIsNone(self.cache.get("foo"))
        self.assertIsNone(self.cache.get("baz"))

if __name__ == '__main__':
    unittest.main()
