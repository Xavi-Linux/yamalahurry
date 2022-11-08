"""
Tests for the yaml parser
"""

import pytest

from yamalahurry.yamala.reader import FileTypeError, PyYamlReader


@pytest.fixture
def instantiate_reader():
    return PyYamlReader()


# #### Happy Path
def test_call(instantiate_reader):
    instantiate_reader.load('/tmp/dir/file.yaml')


# #### Sad Path
@pytest.mark.parametrize(('filepath', 'output'),
                         [
                             (#Test 1
                                 '/home/path/file.xlsx', 'File extension must be .yaml or .yml'
                             )
                         ], ids=['excel_file-str']
                         )
def test_file_ext(instantiate_reader, filepath, output):
    with pytest.raises(FileTypeError) as exp:
        instantiate_reader.load(filepath)

    assert exp.value.args[0] == output
