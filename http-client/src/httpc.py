import re

from httpclient.argparser.ArgParser import ArgParser
from httpclient.http.HttpClient import is_redirect, parse_url, parse_response, parse_status_line, send_request


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


def fix_content_length_header(headers: list, data: str):
    content_length_string = f'Content-Length: {len(data)}'
    pattern = r'^Content-Length:.*'
    replaced = False

    for i in range(len(headers)):
        if re.match(pattern, headers[i]):
            replaced = True
            headers[i] = re.sub(pattern, content_length_string, headers[i])

    if not replaced:
        headers.append(content_length_string)


def adjust_headers(headers: list, host: str):
    fix_host_header(headers, host)

    return '\r\n'.join(headers)


def adjust_request(request_type: str, path: str, http_version_string: str):
    return f'{request_type.upper()} {path} {http_version_string}'


def get_data(args):
    if args.d is None:
        with open(args.f, 'r') as file:
            data = file.read()
        return data
    else:
        return args.d


def print_or_write(body, args):
    if args.o is None:
        print(body)
    else:
        with open(args.o, 'w') as file:
            file.write(body)
        if args.v:
            print(f"** Wrote {len(body)} bytes of data to '{args.o}'")


def get(args):
    (protocol, host, port, path) = parse_url(args.URL)
    request = adjust_request('GET', path, 'HTTP/1.0')
    headers = adjust_headers(args.h, host)
    full_request = f'{request}\r\n{headers}\r\n\r\n'

    if args.v:
        print('Request:')
        print(('> ' + full_request).replace('\r\n', '\r\n> '))

    response = send_request(host, port, full_request)

    (status_line, response_headers, response_body) = parse_response(response)

    if args.v:
        print('Response:')
        print('< ' + status_line)
        print('< ' + '\r\n< '.join(response_headers) + '\r\n< ')

    print_or_write(response_body, args)


def post(args):
    (protocol, host, port, path) = parse_url(args.URL)
    request = adjust_request('POST', path, 'HTTP/1.0')
    data = get_data(args)
    fix_content_length_header(args.h, data)
    headers = adjust_headers(args.h, host)
    full_request = f'{request}\r\n{headers}\r\n\r\n{data}\r\n\r\n'

    if args.v:
        print('Request:')
        print(('> ' + full_request).replace('\r\n', '\r\n> '))

    response = send_request(host, port, full_request)

    (status_line, response_headers, response_body) = parse_response(response)

    (_, response_code, _) = parse_status_line(status_line)

    if args.v:
        print('Response:')
        print('< ' + status_line)
        print('< ' + '\r\n< '.join(response_headers) + '\r\n< ')

    print_or_write(response_body, args)


def show_help(args, parser):
    if args.method == 'get':
        parser.get_get_parser().print_help()
    elif args.method == 'post':
        parser.get_post_parser().print_help()
    else:
        parser.print_help()


if __name__ == '__main__':
    parser = ArgParser()
    args = parser.parse_args()

    if args.command == 'get':
        get(args)
    elif args.command == 'post':
        post(args)
    elif args.command == 'help':
        show_help(args, parser)
    else:
        parser.print_help()

