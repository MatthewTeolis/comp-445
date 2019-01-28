import re
from .exceptions.PortOutOfRangeException import PortOutOfRangeException


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


parse_url('http://httpbin.org:8080/status?arg=something&another=yea%20yea')
(protocol, host, port, path) = parse_url('http://httpbin.org/status/418')


# httpclient = HTTPClient(host, port)
# httpclient.connect()
# print(httpclient.get(path))
# httpclient.disconnect()
