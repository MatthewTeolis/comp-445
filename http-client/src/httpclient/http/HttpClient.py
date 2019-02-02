import re
import socket

from httpclient.exceptions.PortOutOfRangeException import PortOutOfRangeException


class HTTPClient:

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send(self, message: str):
        self.socket.sendall(bytes(message, 'utf-8'))
        return self.socket.recv(4096).decode('utf-8')

    def disconnect(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()


def send_request(host: str, port: int, full_request: str):
    httpc = HTTPClient(host, port)

    httpc.connect()
    response = httpc.send(full_request)
    httpc.disconnect()

    return response


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


def parse_status_line(line: str):
    pattern = r'^(?P<version>.*?) (?P<code>\d{3}) (?P<status>.*?)$'
    match = re.match(pattern, line)

    version = match.group('version')
    code = match.group('code')
    status = match.group('status')

    return version, code, status


def parse_response(response: str):
    response_array = response.split('\r\n')
    status_line_index = 0
    header_line_index = 1
    body_separator = response_array.index('')

    status_line = response_array[status_line_index]
    response_headers_array = response_array[header_line_index:body_separator]
    body = response_array[body_separator + 1]

    return status_line, response_headers_array, body


def is_redirect(http_code: int):
    return http_code == 301 or http_code == 307
