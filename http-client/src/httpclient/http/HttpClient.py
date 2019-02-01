import re
import socket

from httpclient.exceptions.PortOutOfRangeException import PortOutOfRangeException


class HTTPClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send(self, message):
        self.socket.sendall(bytes(message, 'utf-8'))
        return self.socket.recv(4096).decode('utf-8')

    def disconnect(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()


def parse_url(url):
    pattern = r'^(?P<protocol>.*)://(?P<host>.*?)(?::(?P<port>.*?))?(?P<path>/.*)?$'
    match = re.match(pattern, url)

    # always defined
    protocol = match.group('protocol')

    # always defined
    host = match.group('host')

    port = match.group('port')
    if port is None:
        port = 80
    else:
        port = int(port)
    if port < 0 or port > 65535:  # it's not a valid port
        raise PortOutOfRangeException(f"port '{port}' is out of range [0, 65535]")

    path = match.group('path')
    if path is None:
        path = '/'

    return protocol, host, port, path
