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
    ('inputs', 'expected'),
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
        ),
        (#Test 4
            {
                'sheet1': {
                    'rows': [],
                }
            },
            OpenxlpyWriter.process.__doc__
        ),
        (#Test 5
            {
                'sheet1':{
                    'columns':[],
                }
            },
            OpenxlpyWriter.process.__doc__
        ),
        (#Test 6
            {
                'sheet1':{
                    'rows': 1.2,
                    'columns': {}
                }
            },
            OpenxlpyWriter.process.__doc__
        ),
        (#Test 7
            {
                'sheet1':{
                    'rows': [1.2, 3.4, 4.5],
                    'columns': [3, 4, 5]
                }
            },
            OpenxlpyWriter.process.__doc__
        ),
        (#Test 8
            {
                'sheet1':{
                    'rows': [1.2, 3.4, 4.5],
                    'columns': {
                        'column1': [1, 0],
                        'column2': [2, 0],
                        'column3': 1
                    }
                }
            },
            OpenxlpyWriter.process.__doc__
        ),
        (#Test 9
            {
                'sheet1':{
                    'rows': [1.2, 3.4, 4.5],
                    'columns': {
                        'column1': [1, 0, 3],
                        'column2': [2, 0, 3],
                        'column3': [1, 2]
                    }
                }
            },
            OpenxlpyWriter.process.__doc__
        ),
        (#Test 10
            {
                'sheet1':{
                    'rows':[1.2, 3.4, 4.5],
                    'columns': {
                        'column1':[1, 0, 3],
                        'column2':[2, 0, 3],
                        'column3':[1, 2, 3]
                    }
                },
                'sheet2': []
            },
            OpenxlpyWriter.process.__doc__
        ),
        (#Test 11
            {
                'sheet1':{
                    'rows':[1.2, 3.4, 4.5],
                    'columns': {
                        'column1':[1, 0, 3],
                        'column2':[2, 0, 3],
                        'column3':[1, 2, 3]
                    }
                },
                'sheet2': {
                    'rows':[1.2, 3.4, 4.5],
                }
            },
            OpenxlpyWriter.process.__doc__
        ),
        (#Test 12
            {
                'sheet1':{
                    'rows':[1.2, 3.4, 4.5],
                    'columns': {
                        'column1':[1, 0, 3],
                        'column2':[2, 0, 3],
                        'column3':[1, 2, 3]
                    }
                },
                'sheet2':{
                    'columns': {
                        'column1':[1, 0, 3],
                        'column2':[2, 0, 3],
                        'column3':[1, 2, 3]
                    }
                }
            },
            OpenxlpyWriter.process.__doc__
        ),
        (#Test 13
            {
                'sheet1':{
                    'rows': [1.2, 3.4, 4.5],
                    'columns': {
                        'column1': [1, 0, 3],
                        'column2': [2, 0, 3],
                        'column3': [1, 2, 3]
                    }
                },
                'sheet2':{
                    'rows': 1.2,
                    'columns': {
                        'column1': [1, 0, 3],
                        'column2': [2, 0, 3],
                        'column3': [1, 2, 3]
                    }
                }
            },
            OpenxlpyWriter.process.__doc__
        ),
        (#Test 14
            {
                'sheet1':{
                    'rows': [1.2, 3.4, 4.5],
                    'columns':{
                        'column1': [1, 0, 3],
                        'column2': [2, 0, 3],
                        'column3': [1, 2, 3]
                    }
                },
                'sheet2':{
                    'rows': [1.2, 3.4, 4.5],
                    'columns': 1.2
                }
            },
            OpenxlpyWriter.process.__doc__
        ),
        (#Test 15
            {
                'sheet1':{
                    'rows': [1.2, 3.4, 4.5],
                    'columns':{
                        'column1': [1, 0, 3],
                        'column2': [2, 0, 3],
                        'column3': [1, 2, 3]
                    }
                },
                'sheet2':{
                    'rows': [1.2, 3.4, 4.5],
                    'columns':{
                        'column1': [1, 0, 3],
                        'column2': [2, 0, 3],
                        'column3': 'Charmander'
                    }
                }
            },
            OpenxlpyWriter.process.__doc__
        ),
        (#Test 16
            {
                'sheet1':{
                    'rows': [1.2, 3.4, 4.5],
                    'columns':{
                        'column1': [1, 0, 3],
                        'column2': [2, 0, 3],
                        'column3': [1, 2, 3]
                    }
                },
                'sheet2':{
                    'rows': [1.2, 3.4, 4.5],
                    'columns':{
                        'column1': [1, 0, 3],
                        'column2': [2, 0, 3],
                        'column3': [1, 2, 3, 5]
                    }
                }
            },
            OpenxlpyWriter.process.__doc__
        )
    ], ids=[
        'empty-dict-1',
        'list-of-dicts-1',
        'no-dict-for-first-level-values-1',
        'rows-no-columns-1',
        'columns-no-rows-1',
        'rows-value-not-a-list-1',
        'columns-value-not-a-dict-1',
        'columns-dict-values-not-lists-1',
        'column-lists-length-not-equals-rows-length-1',
        'no-dict-for-first-level-values-2',
        'rows-no-columns-2',
        'columns-no-rows-2',
        'rows-value-not-a-list-2',
        'columns-value-not-a-dict-2',
        'columns-dict-values-not-lists-2',
        'column-lists-length-not-equals-rows-length-2'
    ]
)
def test_wrong_input(generate_writer, inputs, expected):
    with pytest.raises(WrongInputStructure) as exp:
        generate_writer.process(input)
    assert expected == exp.value.args[0]
