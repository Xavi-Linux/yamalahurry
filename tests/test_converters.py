"""
Tests for the converter class
"""

import pytest

import sys
from pathlib import Path
from typing import Callable, Dict, List, Literal
from yamalahurry.yamala.converters import PyYamlToOpenpyxlConverter


@pytest.fixture
def files_path_factory(tmp_path) -> Callable:
    dummy_dir: Path = tmp_path / 'test'
    dummy_dir.mkdir()

    def wrapper(files: List[str], element_type: Literal['d', 'f']) -> List[str]:
        fake_paths: List[Path] = []
        for file in files:
            element: Path = dummy_dir / file
            if element_type == 'd':
                element.mkdir()

            elif element_type == 'f':
                element.write_text('1')

            fake_paths.append(element)

        return list(map(lambda f: str(Path(f).resolve()), fake_paths))

    return wrapper


def test_converter_instantiation():
    inputs: Dict = {
        'files': ['.', '../.'],
        'destination': Path('/folder/'),
        'recursive': False
    }
    converter = PyYamlToOpenpyxlConverter(**inputs)
    assert hasattr(converter, 'writer')
    assert hasattr(converter, 'reader')
    assert hasattr(converter, 'read')
    assert hasattr(converter, 'transform')
    assert hasattr(converter, 'write')
    assert hasattr(converter, 'files') and isinstance(converter.files, List)
    assert hasattr(converter, 'destination') and isinstance(converter.destination, Path)
    assert hasattr(converter, 'recursive') and isinstance(converter.recursive, bool)


@pytest.mark.parametrize(
    ('inputs', 'expected'),
    [
        (#Test 1
            [['folder1'], 'd'],
            False
        ),
        (#Test 2
            [['file.yml'], 'f'],
            True
        ),
        (#Test 3
            [['folder2', 'folder3', 'folder4'], 'd'],
            False
        ),
        (#Test 4
            [['file1.yml', 'file2.yml', 'file3.yml'], 'f'],
            True
        )
    ], ids=[
        'one-folder-1',
        'one-file-1',
        'multiple-folders-1',
        'multiple-files-1'
    ]
)
def test_files_param_inspector(files_path_factory, inputs, expected):
    """
    Test whether the converter is able to identify if files argument contains
    files or directories. Additionally, it tests if the converter is casting
    folder paths to Path instances.
    """
    new_inputs: List = files_path_factory(*inputs)

    constructor: Dict = {
        'files': new_inputs,
        'destination': Path('/folder/'),
        'recursive': False
    }
    converter = PyYamlToOpenpyxlConverter(**constructor)

    assert converter._are_files == expected
    assert all(map(lambda f: isinstance(f, Path), converter._converted_files))

# ### Sad Path


@pytest.mark.parametrize(
    ('inputs', 'expected'),
    [
        (#Test 1
            ['folder1', 'folder2'],
            FileNotFoundError
        ),
        (#Test 2
            ['file.yml', 'file2.yml'],
            FileNotFoundError
        )
    ], ids=[
        'missing-folder-1',
        'missing-file-1'
    ]
)
def test_file_does_not_exist(inputs, expected):
    """
    Test whether the converter raises and error when it receives a
    non-existing file.
    """
    constructor: Dict = {
        'files': inputs,
        'destination': Path('/folder/'),
        'recursive': False
    }
    with pytest.raises(expected) as exp:
        _ = PyYamlToOpenpyxlConverter(**constructor)

    assert exp.type == expected
