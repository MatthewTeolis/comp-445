import socket


class HTTPClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def get(self, url):
        request = f"GET {url} HTTP/1.0"
        headers = f"Host: {self.host}"
        self.socket.sendall(bytes(f"{request}\r\n{headers}\r\n\r\n", 'utf-8'))
        return self.socket.recv(4096).decode('utf-8')

    def disconnect(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
