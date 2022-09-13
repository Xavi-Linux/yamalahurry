import pytest

from argparse import ArgumentParser, Namespace
import sys


def args():
    return ['-f']


@pytest.fixture()
def create_parser():
    parser: ArgumentParser = ArgumentParser(description='Yamala Hurry')
    return parser


@pytest.mark.parametrize('arguments',
                         [(['-f', 'val']),
                          (['--folder', 'val']),
                          (['-s'])]
)
def test_parse_arguments(create_parser, monkeypatch, arguments):
    monkeypatch.setattr(sys, 'argv', arguments)
    create_parser.add_argument('-f', '--folder')
    namespace: Namespace = create_parser.parse_args(sys.argv)