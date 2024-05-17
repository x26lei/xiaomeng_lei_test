# Geo Distributed Cache

Geo Distributed Cache is a geographically distributed caching library that supports LRU (Least Recently Used) eviction and TTL (Time to Live) mechanisms. This library is designed for distributed systems to provide efficient data caching and access through geolocation.

## Features

- LRU caching strategy
- TTL expiration mechanism
- Geographically distributed node selection
- Simple client and server implementation

## Installation

You can install this library using `pip`:

```bash
pip install geo_distributed_cache
```
## Usage
On local server:
``` python
from geo_distributed_cache.cache import GeoDistributedCache

nodes = {
    'node1': ('localhost', 5000, 0.0, 0.0),
    'node2': ('localhost', 5001, 10.0, 10.0)
}
cache = GeoDistributedCache(capacity=100, ttl=60, nodes=nodes, location=(5.0, 5.0))

cache.set("Key", "Data")
print(cache.get("Key"))  # Output: Data

```
Start remote servers:
``` python
# server.py
from geo_distributed_cache.server import start_server

if __name__ == "__main__":
    start_server('localhost', 5000)
    start_server('localhost', 5001)
```
## Tests
The tests can be run with 
``` bash
python -m unittest discover -s tests
```