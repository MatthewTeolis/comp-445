import re


def parse_qparams(qparams_list: list):
    qparam_dict = {}

    for qparam in qparams_list:
        qp = qparam.split('=', 1)

        if len(qp) == 1:
            qparam_dict[qp[0]] = True
        else:
            qparam_dict[qp[0]] = qp[1]

    return qparam_dict


def parse_request_line(request: str):
    pattern = r'(?P<verb>.*?) (?P<path>.*?) (?P<version>.*)'
    match = re.match(pattern, request)

    verb = match.group('verb')
    raw_path = match.group('path')
    raw_path_split = raw_path.split('?', 1)
    path = raw_path_split[0]
    qparams = parse_qparams(re.split('&+', raw_path_split[1])) if len(raw_path_split) > 1 else dict()
    version = match.group('version')

    return verb, path, version, qparams


def parse_request(request: str):
    from httpserver.http.HttpRequest import HttpRequest
    from httpserver.util.converter import convert_list_headers_to_dictionary

    request_array = request.split('\r\n')

    request_line_index = 0
    header_line_index = 1
    body_separator = request_array.index('')

    request_line = request_array[request_line_index]
    verb, path, version, qparams = parse_request_line(request_line)

    headers_list = request_array[header_line_index:body_separator]
    headers = convert_list_headers_to_dictionary(headers_list)

    content_array = request_array[body_separator + 1:]
    content = '\r\n'.join(content_array)

    return HttpRequest(verb, path, version, qparams, headers, content)


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
