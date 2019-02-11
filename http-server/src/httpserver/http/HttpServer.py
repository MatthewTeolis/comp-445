import socket


class HttpServer:

    def __init__(self, port: int):
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', port))
        self.clients = list()

    def __recv_all(self):
        total_data = []

        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            total_data.append(data.decode('utf-8'))

        return ''.join(total_data)

    def listen(self):
        self.socket.listen(5)

    def accept(self) -> (socket.socket, str):
        return self.socket.accept()

    def kill(self):
        self.socket.close()
