"""
Test cases for the application entrypoint
"""

import pytest

from yamalahurry.yamala.cli import get_parser

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
                             ),
                             (#Test 5
                                    ['read-folders', 'folder1'],
                                    {'files': ['folder1'], 'destination': Path.cwd(), 'recursive': False}
                             ),
                             (#Test 6
                                    ['read-folders', 'folder1', 'folder2'],
                                    {'files': ['folder1', 'folder2'], 'destination': Path.cwd(), 'recursive': False}
                             ),
                             (#Test 7
                                    ['read-folders', 'folder1', 'folder2', '-d', '/folder/'],
                                    {
                                        'files': ['folder1', 'folder2'],
                                        'destination': Path('/folder/'),
                                        'recursive': False
                                    }
                             ),
                             (#Test 8
                                     ['read-folders', 'folder1', 'folder2', '--destination', '/folder/'],
                                     {
                                         'files':['folder1', 'folder2'],
                                         'destination':Path('/folder/'),
                                         'recursive': False
                                     }
                             ),
                             (#Test 9
                                     ['read-folders', 'folder1', '-r'],
                                     {'files':['folder1'], 'destination':Path.cwd(), 'recursive': True}
                             ),
                             (#Test 10
                                     ['read-folders', 'folder1', '--recursive'],
                                     {'files':['folder1'], 'destination':Path.cwd(), 'recursive': True}
                             ),
                             (#Test 11
                                     ['read-folders', 'folder1', '-d', '/folder/', '-r'],
                                     {
                                         'files':['folder1'],
                                         'destination':Path('/folder/'),
                                         'recursive': True
                                     }
                             ),
                             (#Test 12
                                     ['read-folders', 'folder1', '-d', '/folder/', '--recursive'],
                                     {
                                         'files':['folder1'],
                                         'destination':Path('/folder/'),
                                         'recursive':True
                                     }
                             )
                         ], ids=['read_files-one_file-default_cwd',
                                 'read_files-two_files-default_cwd',
                                 'read_files-two_files-d',
                                 'read_files-two_files-destination',
                                 'read_folders-one_file-default_cwd-default_r',
                                 'read_folders-two_files-default_cwd-default_r',
                                 'read_folders-two_files-d-default_r',
                                 'read_folders-two_files-destination-default_r',
                                 'read_folders-one_file-default_cwd-r',
                                 'read_folders-one_file-default_cwd-recursive',
                                 'read_folders-one_file-d-r',
                                 'read_folders-one_file-d-recursive',
                                 ]
                         )
def test_parser(create_parser, monkey_factory, arguments, expected):
    monkey_factory(arguments)
    namespace: Namespace = create_parser.parse_args(sys.argv)
    assert vars(namespace) == expected
    assert isinstance(namespace.destination, Path)
    assert isinstance(namespace.files, List)
    if hasattr(namespace, 'recursive'):
        assert isinstance(namespace.recursive, bool)

