import socket

from sender.sender import Sender


class HTTPClient:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send(self, message: str):
        self.socket.sendall(bytes(message, 'utf-8'))
        return self.__recv_all()

    def __recv_all(self):
        total_data = []

        while True:
            data = self.socket.recv(1024)
            if not data:
                break
            total_data.append(data.decode('utf-8'))

        return ''.join(total_data)

    def disconnect(self):
        self.socket.close()


def send_request(host: str, port: int, full_request: str):
    # httpc = HTTPClient(host, port)

    # httpc.connect()
    # response = httpc.send(full_request)
    # httpc.disconnect()

    sender = Sender(host, port, 'localhost', 3000)
    response = sender.send_data(full_request)
    sender.close()

    return response


def is_redirect(http_code: int):
    return http_code in [301, 302, 307]
