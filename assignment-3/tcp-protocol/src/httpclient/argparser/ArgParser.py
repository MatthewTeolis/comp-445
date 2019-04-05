from argparse import ArgumentParser


class ArgParser:

    def __init__(self):
        self.parser = ArgumentParser(
            prog='httpc',
            usage='httpc command [arguments]',
            description='httpc is a curl-like application but supports HTTP protocol only.',
            epilog='Use "httpc help [command]" for more information about a command.',
            add_help=False
        )

        # create the top-level parser
        subparsers = self.parser.add_subparsers(title='Commands', metavar='', dest='command')

        # create the parser for the "get" command
        self.get_parser = subparsers.add_parser(
            'get',
            usage='httpc get [-v] [-h key:value] URL',
            description='Get executes a HTTP GET request for a given URL.',
            help='executes a HTTP GET request and prints the response.',
            add_help=False
        )
        self.get_parser.add_argument('URL', type=str)
        self.get_parser.add_argument('-v', action='store_true', help='Prints the detail of the response such as protocol, status, and headers.')
        self.get_parser.add_argument('-h', type=str, default=[], action='append', metavar='key:value', help="Associates headers to HTTP Request with the format 'key:value'")
        self.get_parser.add_argument('-o', type=str, metavar='file', help='Writes the output to a file instead of stdout.')

        # create the parser for the "post" command
        self.post_parser = subparsers.add_parser(
            'post',
            usage='httpc post [-v] [-h key:value] [-d inline-data] [-f file] URL',
            description='Post executes a HTTP POST request for a given URL with inline data or from file.',
            help='executes a HTTP POST request and prints the response.',
            epilog='Either [-d] or [-f] can be used but not both.',
            add_help=False
        )
        self.post_parser.add_argument('URL', type=str)
        self.post_parser.add_argument('-v', action='store_true', help='Prints the detail of the response such as protocol, status, and headers.')
        self.post_parser.add_argument('-h', type=str, default=[], action='append', metavar='key:value', help="Associates headers to HTTP Request with the format 'key:value'")
        self.post_parser.add_argument('-o', type=str, metavar='file', help='Writes the output to a file instead of stdout.')
        data_option = self.post_parser.add_mutually_exclusive_group(required=True)
        data_option.add_argument('-d', type=str, metavar='string', help='Associates an inline data to the body HTTP POST request.')
        data_option.add_argument('-f', type=str, metavar='file', help='Associates the content of a file to the body HTTP POST request.')

        # create the parser for the "help" command
        self.help_parser = subparsers.add_parser('help', help='prints this screen.', add_help=False)
        self.help_parser.add_argument('method', nargs='?')

    def parse_args(self):
        return self.parser.parse_args()

    def get_get_parser(self):
        return self.get_parser

    def get_post_parser(self):
        return self.post_parser

    def get_help_parser(self):
        return self.help_parser

    def get_parser(self):
        return self.parser

    def print_help(self):
        self.parser.print_help()
