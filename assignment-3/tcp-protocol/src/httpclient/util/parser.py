import re


def parse_header(header: str):
    match = re.match(r'(?P<key>.*?):\s*(?P<value>.*)', header)

    if match is not None:
        key = match.group('key')
        value = match.group('value')
        return key, value

    return None


def parse_status_line(line: str):
    pattern = r'^(?P<version>.*?) (?P<code>\d{3}) (?P<status>.*?)$'
    match = re.match(pattern, line)

    version = match.group('version')
    code = match.group('code')
    status = match.group('status')

    return version, int(code), status


def parse_response(response: str):
    from httpclient.http.HttpResponse import HttpResponse
    from httpclient.util.converter import convert_list_headers_to_dictionary

    response_array = response.split('\r\n')
    status_line_index = 0
    header_line_index = 1
    body_separator = response_array.index('')

    status_line = response_array[status_line_index]
    version, code, status = parse_status_line(status_line)

    headers_list = response_array[header_line_index:body_separator]
    headers = convert_list_headers_to_dictionary(headers_list)

    body_array = response_array[body_separator + 1:]
    body = '\r\n'.join(body_array)

    return HttpResponse(version, code, status, headers, body)


def parse_url(url):
    from httpclient.exceptions.PortOutOfRangeException import PortOutOfRangeException

    pattern = r'(?:^(?P<protocol>.*)://)?(?P<host>.*?)(?::(?P<port>.*?))?(?P<path>/.*)?$'
    match = re.match(pattern, url)

    protocol = match.group('protocol')

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
