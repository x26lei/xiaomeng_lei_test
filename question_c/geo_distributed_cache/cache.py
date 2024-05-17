import time
import threading
from collections import OrderedDict
from typing import Any, Optional, Dict, Tuple
import socket
import pickle
import math

class LRUCache:
    def __init__(self, capacity: int, ttl: int):
        self.cache = OrderedDict() # OrdererDict allows the LRU evict operation
        self.capacity = capacity # the cache has a fixed capacity
        self.ttl = ttl # each item in cache has a fixed time to live
        self.lock = threading.Lock() # provide thread safety if multiple use access the cache on the same node
        self.expiry_times = {}

    def _evict(self):
        while len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def _cleanup(self):
        current_time = time.time()
        keys_to_delete = [key for key, expiry in self.expiry_times.items() if expiry <= current_time]
        for key in keys_to_delete:
            del self.cache[key]
            del self.expiry_times[key]

    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            self._cleanup() # run clean up func once before every get call
            if key in self.cache:
                self.cache.move_to_end(key)
                return self.cache[key]
            return None

    def set(self, key: str, value: Any):
        with self.lock:
            self._cleanup()
            self.cache[key] = value
            self.cache.move_to_end(key) # recently accessed item are moved to the end to allow LRU evict from the start
            self.expiry_times[key] = time.time() + self.ttl
            self._evict()

class GeoDistributedCache:
    def __init__(self, capacity: int, ttl: int, nodes: Dict[str, Tuple[str, int, float, float]], location: Tuple[float, float]):
        self.local_cache = LRUCache(capacity, ttl)
        self.nodes = nodes  # Dictionary of {node_name: (host, port, x, y)}
        self.location = location  # current node's location is (x, y)
    
    def get_closest_node(self) -> str:
        # this function recalculate the distance, since the logic of node proximity is undefined
        # which can be replaced by adding a distance table for look-up
        closest_node = None
        min_distance = float('inf')
        for node_name, (host, port, node_x, node_y) in self.nodes.items():
            distance = self._calculate_distance(self.location[0], self.location[1], node_x, node_y)
            if distance < min_distance:
                min_distance = distance
                closest_node = node_name
        return closest_node

    def set(self, key: str, value: Any):
        self.local_cache.set(key, value)
        # send the data to all other nodes to allow high availability and data consistency
        self._replicate_to_other_nodes(key, value)

    def get(self, key: str) -> Optional[Any]:
        value = self.local_cache.get(key)
        if value is not None:
            return value
        closest_node = self.get_closest_node() # closest reference
        return self._fetch_from_node(closest_node, key)

    def _calculate_distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        # use Euclidean distance for simplicity
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def _replicate_to_other_nodes(self, key: str, value: Any):
        for node_name, (host, port, _, _) in self.nodes.items():
            threading.Thread(target=self._send_to_node, args=(host, port, key, value)).start()

    def _send_to_node(self, host: str, port: int, key: str, value: Any):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(pickle.dumps((key, value))) # serialize before sending
        except Exception as e:
            # handling connection error
            print(f"Failed to send to node {host}:{port} - {e}".encode('utf-8', errors='replace'))

    def _fetch_from_node(self, node: str, key: str) -> Optional[Any]:
        host, port, _, _ = self.nodes[node]
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(pickle.dumps(key)) # serialize before sending
                data = s.recv(1024)
                return pickle.loads(data) # deserialize after receiving
        except Exception as e:
            # handling connection error
            print(f"Failed to fetch from node {host}:{port} - {e}".encode('utf-8', errors='replace'))
            return None
