"""
Entrypoint for the client application
"""

from argparse import ArgumentParser, Namespace
from pathlib import Path


def get_parser() -> ArgumentParser:
    """
    Method to instantiate the parser
    """
    parse:ArgumentParser = ArgumentParser(
                                            description='A yaml reader that stores differences in list-like attributes'
                                                        ' in an Excel file',
                                            epilog='Thank you for using Yamala Hurry!',
                                            prog='yamala'
                                          )
    subparser = parse.add_subparsers(title='subcommands', description='Available subcommands')

    parser_files = subparser.add_parser('read-files', help='Subcommand to process one file or a list of them')
    parser_files.add_argument(
                                'files', nargs='+',
                                help='Space-separated list containing file paths with yaml extension.'
                             )
    parser_files.add_argument(
                                '-d', '--destination', dest='destination', default=Path.cwd(), type=Path,
                                help='Folder path in which the output will be stored. It defaults to the current'
                                     ' working directory.'
                              )

    parser_folder = subparser.add_parser(
                                            name='read-folders',
                                            help='Subcommand to process one folder or a list of them'
                                         )
    parser_folder.add_argument(
                                'files', nargs='+', metavar='folders',
                                help='Space-separated list containing folder paths.'
                               )
    parser_folder.add_argument(
                                '-d', '--destination', dest='destination', default=Path.cwd(), type=Path,
                                help='Folder path in which the output will be stored. It defaults to the current'
                                     ' working directory.'
                              )
    parser_folder.add_argument(
                                '-r', '--recursive', dest='recursive', default=False, action='store_true',
                                help='If the flag is raised, it will recursively search for files in the specified'
                                     ' folders. It defaults to False.'
                               )

    return parse


if __name__ == '__main__':

    parser: ArgumentParser = get_parser()
    namespace: Namespace = parser.parse_args()
