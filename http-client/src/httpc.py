import re

from argparser.ArgParser import ArgParser


parser = ArgParser()
args = parser.parse_args()


def construct_headers(headers: list):
    headers_string = "\r\n".join(headers)
    return headers_string


def is_host_header(header: str):
    pattern = r'Host:.*'
    return re.match(pattern, header) is not None


def adjust_headers(headers: list, host: str):
    headers_string = ''
    host_found = False

    for header in headers:
        headers_string += f'\r\n{header}'
        if is_host_header(header):
            host_found = True

    if not host_found:
        return f'Host: {host}\r\n{headers_string}'

    return headers_string



def get(args):
    print(args)
    # (protocol, host, port, path) = parse_url(args.url)
    # headers = adjust_headers(args.h, host)
    # print(headers)



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
