"""
Test file for the Writer Classes
"""
import pytest
from pathlib import Path

from yamalahurry.yamala.writer import OpenxlpyWriter, WrongInputStructure


@pytest.fixture
def make_folder(tmp_path):
    folder = tmp_path / 'tests'
    folder.mkdir()
    return folder


@pytest.fixture
def generate_writer(make_folder):
    return OpenxlpyWriter(make_folder)


# ### Happy path
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


@pytest.mark.parametrize(
    ('inputs', 'sheets_count', 'sheets_names'),
    [
        (#Test 1
            {
                'roles':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                }
            },
            1,
            ['roles']
        ),
        (#Test 2
            {
                'roles':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
                'ro\\les':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
            },
            2,
            ['roles', 'ro_les']
        ),
        (#Test 3
            {
                'roles':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
                'ro/les':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
            },
            2,
            ['roles', 'ro_les']
        ),
        (#Test 4
            {
                'roles':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
                'ro*les':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
            },
            2,
            ['roles', 'ro_les']
        ),
        (#Test 5
            {
                'roles':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
                'ro[les':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
            },
            2,
            ['roles', 'ro_les']
        ),
        (#Test 6
            {
                'roles':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
                'ro]les':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
            },
            2,
            ['roles', 'ro_les']
        ),
        (#Test 7
            {
                'roles':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
                'ro:les':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
            },
            2,
            ['roles', 'ro_les']
        ),
        (#Test 8
            {
                'roles':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
                'ro?les':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
            },
            2,
            ['roles', 'ro_les']
        ),
        (#Test 9
            {
                'roles':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
                'ro?les':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
                'ro[les':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                },
            },
            3,
            ['roles', 'ro_les', 'ro_les_1']
        ),
        (#Test 10
            {
               'b' + 'a' * 35:{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                }
            },
            1,
            ['a' * 31]
        ),
    ], ids=[
        'single-sheet-1',
        'forbidden-symbol-1',
        'forbidden-symbol-2',
        'forbidden-symbol-3',
        'forbidden-symbol-4',
        'forbidden-symbol-5',
        'forbidden-symbol-6',
        'forbidden-symbol-7',
        'two-forbidden-symbols-1',
        'a-too-large-name-for-a-sheet-1'
    ]
)
def test_excel_sheet_creation(generate_writer, inputs, sheets_count, sheets_names):
    generate_writer.process(inputs)
    assert sheets_count == len(generate_writer.workbook.worksheets)
    assert sheets_names == generate_writer.workbook.sheetnames


@pytest.mark.parametrize(
    ('inputs', 'expected'),
    [
        (#Test 1
            'file',
            'file'
        ),
        (#Test 2
            'file' + chr(10),
            'file_'
        ),
        (#Test 3
            'file' + chr(13),
            'file_'
        ),
        (#Test 4
            'file' + '~',
            'file_'
        ),
        (#Test 5
            'file' + '"',
            'file_'
        ),
        (#Test 6
            'file' + '#',
            'file_'
        ),
        (#Test 7
            'file' + '%',
            'file_'
        ),
        (#Test 8
            'file' + '&',
            'file_'
        ),
        (#Test 9
            'file' + '*',
            'file_'
        ),
        (#Test 10
            'file' + ':',
            'file_'
        ),
        (#Test 11
            'file' + '<',
            'file_'
        ),
        (#Test 12
            'file' + '>',
            'file_'
        ),
        (#Test 13
            'file' + '?',
            'file_'
        ),
        (#Test 14
            'file' + '{',
            'file_'
        ),
        (#Test 15
            'file' + '|',
            'file_'
        ),
        (#Test 16
            'file' + '}',
            'file_'
        ),
        (#Test 17
            'file' + '/',
            'file_'
        ),
        (#Test 18
            'file' + '\\',
            'file_'
        ),
        (#Test 19
            'file' + '[',
            'file_'
        ),
        (#Test 4
            'file' + ']',
            'file_'
        )
    ], ids=[
        'simple-file-1',
        'forbidden-char-1',
        'forbidden-char-2',
        'forbidden-char-3',
        'forbidden-char-4',
        'forbidden-char-5',
        'forbidden-char-6',
        'forbidden-char-7',
        'forbidden-char-8',
        'forbidden-char-9',
        'forbidden-char-10',
        'forbidden-char-11',
        'forbidden-char-12',
        'forbidden-char-13',
        'forbidden-char-14',
        'forbidden-char-15',
        'forbidden-char-16',
        'forbidden-char-17',
        'forbidden-char-18',
        'forbidden-char-19'
    ]
)
def test_excel_save(generate_writer, inputs, expected):
    content = {
                'roles':{
                    'rows':['reader', 'editor', 'creator'],
                    'columns':{
                        'user1':[1, 0, 0],
                        'user2':[0, 1, 0],
                        'user3':[1, 1, 0]
                    }
                }
    }

    generate_writer.process(content)
    generate_writer.save(inputs)
    final_file = expected + '.xlsx'
    assert (generate_writer.folderpath / final_file).exists()
    assert '.xlsx' == (generate_writer.folderpath / final_file).suffix


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
