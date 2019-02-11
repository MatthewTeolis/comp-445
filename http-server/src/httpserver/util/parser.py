import re


def parse_request_line(request: str):
    pattern = r'(?P<verb>.*?) (?P<path>.*?) (?P<version>.*)'
    match = re.match(pattern, request)

    verb = match.group('verb')
    path = match.group('path')
    version = match.group('version')

    return verb, path, version


def parse_request(request: str):
    from httpserver.http.HttpRequest import HttpRequest
    from httpserver.util.converter import convert_list_headers_to_dictionary

    request_array = request.split('\r\n')

    request_line_index = 0
    header_line_index = 1
    body_separator = request_array.index('')

    request_line = request_array[request_line_index]
    verb, path, version = parse_request_line(request_line)

    headers_list = request_array[header_line_index:body_separator]
    headers = convert_list_headers_to_dictionary(headers_list)

    content_array = request_array[body_separator + 1:]
    content = '\r\n'.join(content_array)

    return HttpRequest(verb, path, version, headers, content)



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
    from httpserver.http.HttpResponse import HttpResponse
    from httpserver.util.converter import convert_list_headers_to_dictionary

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
