import pytest

from yamalahurry.parser import get_parser

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List
import sys


@pytest.fixture()
def create_parser():
    parser: ArgumentParser = get_parser()

    return parser


@pytest.fixture
def monkey_factory(monkeypatch):

    def get_cwd():
        return Path('/mock/cwd')

    def wrapper(data: List):
        monkeypatch.setattr(sys, 'argv', data)
        monkeypatch.setattr(Path, 'cwd', get_cwd)

    return wrapper


@pytest.mark.parametrize(('arguments', 'expected'),
                         [
                             (#Test 1
                                     ['read-files', 'file1'],
                                     {'files': ['file1'], 'destination': Path.cwd()}
                             ),
                             (#Test 2
                                     ['read-files', 'file1', 'file2'],
                                     {'files': ['file1', 'file2'], 'destination': Path.cwd()}
                             ),
                             (#Test 3
                                     ['read-files', 'file1', 'file2', '-d', '/folder/'],
                                     {'files': ['file1', 'file2'], 'destination': Path('/folder/')}
                             ),
                             (#Test 4
                                     ['read-files', 'file1', 'file2', '--destination', '/folder/'],
                                     {'files': ['file1', 'file2'], 'destination': Path('/folder/')}
                             )
                         ], ids=['one_file-default_cwd',
                                 'two_files-default_cwd',
                                 'two_files-d',
                                 'two_files-destination'
                                 ]
                         )
def test_readfiles(create_parser, monkey_factory, arguments, expected):
    monkey_factory(arguments)
    namespace: Namespace = create_parser.parse_args(sys.argv)
    assert vars(namespace) == expected
    assert isinstance(namespace.destination, Path)
    assert isinstance(namespace.files, List)

def test_rea

