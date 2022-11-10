"""
Test file for the Writer Classes
"""
import pytest
from pathlib import Path

from yamalahurry.yamala.writer import OpenxlpyWriter, WrongInputStructure


@pytest.fixture
def make_folder(tmp_path):
    folder = tmp_path / 'tests'
    return folder.mkdir()


@pytest.fixture
def generate_writer(make_folder):
    return OpenxlpyWriter(make_folder)


@pytest.mark.parametrize(
    ('folder_path', 'expected_type'),
    [
        (#Test1
            Path('/home/path'), Path
        ),
        (#Test2
            '/home/path', Path
        )
    ], ids=[
          'Path-as-folderpath',
          'str-as-folder-path'
    ]
)
def test_instantiation(generate_writer, folder_path, expected_type):
    writer = OpenxlpyWriter(folder_path)
    assert isinstance(writer.folderpath, expected_type)
    if isinstance(folder_path, str):
        folder_path = Path(folder_path)
    assert folder_path == writer.folderpath
    assert hasattr(writer, 'workbook')


# ### Sad path
@pytest.mark.parametrize(
    ('input', 'expected'),
    [
        (#Test 1
            {},
            OpenxlpyWriter.process.__doc__
        ),
        (#Test 2
            [{}, {}],
            OpenxlpyWriter.process.__doc__
        ),
        (#Test 3
            {
                'sheet1': {},
                'sheet2': []
            },
            OpenxlpyWriter.process.__doc__
        )
    ], ids=[
        'empty-dict-1',
        'list-of-dicts-1',
        'no-dict-for-first-level-values-1'
    ]
)
def test_wrong_input(generate_writer, input, expected):
    with pytest.raises(WrongInputStructure) as exp:
        generate_writer.process(input)
    assert expected == exp.value.args[0]
