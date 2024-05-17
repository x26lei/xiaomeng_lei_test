import socket
import threading
import pickle

# this setup uses a shared dictionary as the cache for remote nodes for simplicity
# it can be replaced by constructing a GeoDistributedCache instance for each node
cache = {} 

def handle_client_connection(client_socket):
    try:
        data = client_socket.recv(1024)
        key_value = pickle.loads(data)
        if isinstance(key_value, tuple) and len(key_value) == 2:
            key, value = key_value
            print(f"Received set request: {key} -> {value}")
            cache[key] = value
        elif isinstance(key_value, str):
            key = key_value
            value = cache.get(key, None)
            print(f"Received get request: {key} -> {value}")
            client_socket.sendall(pickle.dumps(value))
    except Exception as e:
        print(f"Error handling client connection: {e}")
    finally:
        client_socket.close()

def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server started on {host}:{port}")
    
    while True:
        client_sock, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client_connection, args=(client_sock,))
        client_handler.start()
