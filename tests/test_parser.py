import pytest

from yamalahurry.parser import get_parser

from argparse import ArgumentParser, Namespace
from typing import List
import sys


@pytest.fixture()
def create_parser():
    parser: ArgumentParser = get_parser()

    return parser


@pytest.fixture
def monkey_factory(monkeypatch):
    def wrapper(data: List):
        monkeypatch.setattr(sys, 'argv', data)

    return wrapper


@pytest.mark.parametrize('arguments',
                         [(['-f', 'val']),
                          (['--folder', 'val'])
                         ])
def test_folder_arguments(create_parser, monkey_factory, arguments):
    monkey_factory(arguments)
    namespace: Namespace = create_parser.parse_args(sys.argv)
    assert 'folder' in namespace
