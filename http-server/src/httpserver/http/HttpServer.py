import socket


class HttpServer:

    def __init__(self, port: int):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', port))

    def listen(self):
        self.socket.listen(5)

    def accept(self) -> (socket.socket, str):
        return self.socket.accept()

    def kill(self):
        self.socket.close()
