"""
Entrypoint for the client application
"""
from argparse import ArgumentParser, Namespace
from pathlib import Path


def get_parser() -> ArgumentParser:
    parse:ArgumentParser = ArgumentParser(description='Yamala Hurry')
    subparser = parse.add_subparsers(title='subcommands', description='available subcommands')

    parser_files = subparser.add_parser('read-files', help='')
    parser_files.add_argument('files', nargs='+')
    parser_files.add_argument('-d', '--destination', dest='destination', default=Path.cwd(), type=Path)

    #parser_folder = subparser.add_parser(name='read-folder', help='')
    return parse


if __name__ == '__main__':

    parser: ArgumentParser = get_parser()
    namespace: Namespace = parser.parse_args()
