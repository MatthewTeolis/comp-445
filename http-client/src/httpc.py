import re

from httpclient.argparser.ArgParser import ArgParser
from httpclient.http.HttpClient import parse_url
from httpclient.http.HttpClient import HTTPClient


def fix_connection_header(headers: list):
    connection_close_string = 'Connection: close'
    pattern = r'^Connection:.*'
    replaced = False

    for i in range(len(headers)):
        if re.match(pattern, headers[i]):
            replaced = True
            headers[i] = re.sub(pattern, connection_close_string, headers[i])

    if not replaced:
        headers.append(connection_close_string)


def fix_host_header(headers: list, host: str):
    # if it does not have the Host string in the headers
    if not any(re.match('^Host:.*', header) is not None for header in headers):
        # append the default host value
        headers.append(f'Host: {host}')


def adjust_headers(headers: list, host: str):
    fix_host_header(headers, host)
    fix_connection_header(headers)

    return '\r\n'.join(headers)


def adjust_request(request_type: str, path: str, http_version_string: str):
    return f'{request_type.upper()} {path} {http_version_string}'


def parse_status_line(line: str):
    pattern = r'^(?P<http_version>.*?) (?P<http_code>\d{3}) (?P<http_status>.*?)$'
    match = re.match(pattern, line)
    http_version = match.group('http_version')
    http_code = match.group('http_code')
    http_status = match.group('http_status')

    return http_version, http_code, http_status


def parse_response(response: str):
    response_array = response.split('\r\n')
    status_line_index = 0
    header_line_index = 1
    body_separator = response_array.index('')

    status_line = response_array[status_line_index]
    response_headers_array = response_array[header_line_index:body_separator]
    body = response_array[body_separator + 1]

    print("status line", status_line)
    print("headers", response_headers_array)
    print("body ", body)


def get(args):
    (protocol, host, port, path) = parse_url(args.URL)
    request = adjust_request('GET', path, 'HTTP/1.0')
    headers = adjust_headers(args.h, host)
    full_request = f'{request}\r\n{headers}\r\n\r\n'

    httpc = HTTPClient(host, port)
    httpc.connect()
    response = httpc.send(full_request)
    httpc.disconnect()

    parse_response(response)

    # print(response)


parser = ArgParser()
args = parser.parse_args()


def show_help(args):
    if args.method is None:
        parser.print_help()
    elif args.method == 'get':
        parser.get_get_parser().print_help()
    elif args.method == 'post':
        parser.get_post_parser().print_help()


if args.command == 'get':
    get(args)
elif args.command == 'post':
    print(args)
elif args.command == 'help':
    show_help(args)
else:
    parser.print_help()


# httpclient = HTTPClient(host, port)
# httpclient.connect()
# print(httpclient.get(path))
# httpclient.disconnect()
