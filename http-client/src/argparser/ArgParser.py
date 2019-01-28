import argparse

parser = argparse.ArgumentParser(
    prog='httpc',
    # usage='httpc command [arguments]',
    description='httpc is a curl-like application but supports HTTP protocol only.',
    epilog='Use "httpc help [command]" for more information about a command.',
    add_help=False
)
# g = parser.add_mutually_exclusive_group()

# get_subparser = parser.add_subparsers('get', help='executes a HTTP GET request and prints the response.')
# post_subparser = parser.add_subparsers('post', help='executes a HTTP POST request and prints the response.')
# help_subparser = parser.add_subparsers('help', help='prints this screen.')

# g.add_argument('get', help='executes a HTTP GET request and prints the response.')
# g.add_argument('post', help='executes a HTTP POST request and prints the response.')
# g.add_argument('help', help='prints this screen.')

# create the top-level parser
subparsers = parser.add_subparsers(title='Commands', metavar='')

# create the parser for the "command_1" command
parser_a = subparsers.add_parser('get', help='executes a HTTP GET request and prints the response.')
parser_a.add_argument('url', type=str, help='help for bar, positional')

# create the parser for the "command_2" command
parser_b = subparsers.add_parser('post', help='executes a HTTP POST request and prints the response.')
parser_b.add_argument('b', type=str, help='help for b')
parser_c = subparsers.add_parser('help', help='prints this screen.')


parser.print_help()
# args = parser.parse_args()
# print(args)


######
# httpc help
#     httpc is a curl-like application but supports HTTP protocol only.
# Usage:
#     httpc command [arguments]
# The commands are:
#     get executes a HTTP GET request and prints the response.
#     post executes a HTTP POST request and prints the response.
#     help prints this screen.
#
# Use "httpc help [command]" for more information about a command.
