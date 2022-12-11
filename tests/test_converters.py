"""
Tests for the converter class
"""

import pytest

from pathlib import Path
from typing import Callable, Dict, List, Literal, Union
from yamalahurry.yamala.converters import PyYamlToOpenpyxlConverter


@pytest.fixture
def files_path_factory(tmp_path) -> Callable:
    dummy_dir: Path = tmp_path / 'test'
    dummy_dir.mkdir()

    def wrapper(files: List[str], element_type: Literal['d', 'f'], text: Union[None, str] = None) -> List[str]:
        fake_paths: List[Path] = []
        for file in files:
            element: Path = dummy_dir / file
            if element_type == 'd':
                element.mkdir()

            elif element_type == 'f':
                if text:
                    element.write_text(text)

                else:
                    element.write_text('1')

            fake_paths.append(element)

        return list(map(lambda f: str(Path(f).resolve()), fake_paths))

    return wrapper


@pytest.fixture
def create_nested_folders(tmp_path) -> Callable:
    dummy_dir: Path = tmp_path / 'folder_test'
    dummy_dir.mkdir()

    def wrapper(
            fake_folders: List[str], dir_depths: List[int],
            num_yaml_files: List[int], num_non_yaml: List[int]
     ) -> List[str]:
        new_folders: List[Path] = []
        for fake_folder, depth, yamls, non_yamls in zip(fake_folders, dir_depths, num_yaml_files, num_non_yaml):
            new_folder: Path = dummy_dir / fake_folder
            new_folder.mkdir()
            new_folders.append(new_folder)
            for d in range(0, depth + 1):
                if d > 0:
                    new_folder = new_folder / 'test{0}'.format(str(d))
                    new_folder.mkdir()

                for y in range(0, yamls):
                    new_yaml = new_folder / 'file{0}.yaml'.format(str(y))
                    new_yaml.write_text('1')

                for ny in range(0, non_yamls):
                    new_non_yaml = new_folder / 'file{0}.txt'.format(str(y))
                    new_non_yaml.write_text('2')

        return list(map(lambda f: str(Path(f).resolve()), new_folders))

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


@pytest.mark.parametrize(
    ('fixture_name', 'inputs', 'recursive', 'expected'),
    [
        (#Test 1
            'files_path_factory',
            [['file1.yml'], 'f', 'hello'],
            False,
            1
        ),
        (#Test 2
            'files_path_factory',
            [['file2.yaml', 'file1.yml', 'file3.yaml'], 'f', 'hello'],
            False,
            3
        ),
        (#Test 3
            'create_nested_folders',
            [['no_depth'],[0],[5],[3]],
            False,
            5
        ),
        (#Test 4
            'create_nested_folders',
            [['folder1', 'folder2', 'folder3'], [0, 0, 0], [7, 3, 2],[1, 10, 9]],
            False,
            12
        ),
        (#Test 5
            'create_nested_folders',
            [['folder1'], [1], [4], [2]],
            True,
            8
        ),
        (#Test 6
            'create_nested_folders',
            [['folder1', 'folder2'], [1, 1], [4, 4], [7, 7]],
            True,
            16
        ),
        (#Test 7
            'create_nested_folders',
            [['folder1', 'folder2', 'folder3'], [2, 2, 2], [3, 3, 3], [1, 2, 3]],
            True,
            27
        ),
        (#Test 8
            'create_nested_folders',
            [['folder1'], [5], [8], [3]],
            False,
            8
        ),
        (#Test 9
            'create_nested_folders',
            [['folder1', 'folder2', 'folder3'], [1, 2, 4], [5, 4, 3], [6, 7, 8]],
            True,
            37
        )
    ], ids=[
        'single-file-1',
        'multiple-files-1',
        'one-folder-5-files-no-depth-1',
        'multiple-folders-multiple-files-no-depth-1',
        'one-folder-4-files-depth-1-1',
        'multiple-folders-4-files-depth-1-1',
        'multiple-folders-3-files-depth-2-1',
        'depth-3-recursive-false-1',
        'multiple-folders-different-depths-1'

    ]
)
def test_read_method(fixture_name, inputs, recursive, expected, request):
    """
    Test whether every target file is read and loaded into an iterable data structure.
    """
    fixture_callable: Callable = request.getfixturevalue(fixture_name)
    new_inputs: List = fixture_callable(*inputs)

    constructor: Dict = {
        'files': new_inputs,
        'destination': Path('/folder/'),
        'recursive': recursive
    }
    converter = PyYamlToOpenpyxlConverter(**constructor)

    converter.read()
    assert converter.processed_files == expected


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
