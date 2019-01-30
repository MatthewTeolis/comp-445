from argparser.ArgParser import ArgParser


parser = ArgParser()
args = parser.parse_args()


def get(args):
    print("get was called with", args)


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
