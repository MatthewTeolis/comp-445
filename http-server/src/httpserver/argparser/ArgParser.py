import os
from argparse import ArgumentParser


class ArgParser:

    def __init__(self):
        self.parser = ArgumentParser(
            prog='httpfs',
            usage='httpfs [-v] [-p PORT] [-d PATH-TO-DIR]',
            # add_help=False
        )

        # self.parser.add_argument(
        #     '-h',
        #     '--help',
        #     action='store_true',
        #     help='Show this help message and exit.',
        #     dest='help'
        # )
        self.parser.add_argument(
            '-v',
            action='store_true',
            help='Prints debugging messages.',
            dest='verbose'
        )
        self.parser.add_argument(
            '-p',
            metavar='',
            type=int,
            default=8080,
            help='Specifies the port number that the server will listen and serve at. Default is 8080.',
            dest='port'
        )
        self.parser.add_argument(
            '-d',
            metavar='',
            type=str,
            default=os.getcwd(),
            help='Specifies the directory that the server will use to read/write requested files. '
                 'Default is the current directory when launching the application.',
            dest='directory'
        )
        self.parser.add_argument(
            '-o',
            action='store_true',
            help='Overwrites file with request\'s content.',
            dest='overwrite'
        )

    def parse_args(self):
        return self.parser.parse_args()

    def get_parser(self):
        return self.parser

    def print_help(self):
        self.parser.print_help()
