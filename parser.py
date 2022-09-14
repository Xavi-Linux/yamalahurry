from argparse import ArgumentParser, Namespace


def get_parser() -> ArgumentParser:
    parse:ArgumentParser = ArgumentParser(description='Yamala Hurry', prog='yamala')
    parse.add_argument('-f', '--folder', default=None, dest='folder')

    return parse


if __name__ == '__main__':

    parser: ArgumentParser = get_parser()
    namespace: Namespace = parser.parse_args()
