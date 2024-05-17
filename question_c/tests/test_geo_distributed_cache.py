import unittest
import threading
import time
from geo_distributed_cache.cache import GeoDistributedCache
from server.server import start_server

def start_server_in_thread(host, port):
    server = threading.Thread(target=start_server, args=(host, port))
    server.daemon = True
    server.start()
    time.sleep(1)  # wait for server to start
    return server

class TestGeoDistributedCacheIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodes = {
            'node1': ('localhost', 5000, 0.0, 0.0),
            'node2': ('localhost', 5001, 10.0, 10.0)
        }

        cls.server_thread1 = start_server_in_thread('localhost', 5000)
        cls.server_thread2 = start_server_in_thread('localhost', 5001)

        cls.cache = GeoDistributedCache(capacity=100, ttl=60, nodes=cls.nodes, location=(5.0, 5.0))

    @classmethod
    def tearDownClass(cls):
        pass

    def test_set_and_get(self):
        self.cache.set("foo", "bar")
        value = self.cache.get("foo")
        self.assertEqual(value, "bar")

    def test_set_and_get_from_remote_node(self):
        self.cache.set("hello", "world")
        value = self.cache.get("hello")  # This request will be fetched from the nearest node
        self.assertEqual(value, "world")

if __name__ == '__main__':
    unittest.main()
