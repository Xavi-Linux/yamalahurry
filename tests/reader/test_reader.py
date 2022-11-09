"""
Tests for the yaml parser
"""

import pytest

from yamalahurry.yamala.reader import FileTypeError, PyYamlReader
from typing import Iterable
from textwrap import dedent


# #### Fixtures
@pytest.fixture
def instantiate_pyyaml_reader():
    return PyYamlReader()


@pytest.fixture
def build_temp_file_factory(tmp_path):
    folder = tmp_path / 'test_files'
    folder.mkdir()

    def wrapper(text: str, file_name: str):
        filepath = folder / file_name
        filepath.write_text(text)

        return filepath

    return wrapper


# #### Happy Path
@pytest.mark.parametrize(('text', 'name', 'expected'),
                         [
                              (#Test 1
                                """
                                a: 1
                                b: 2
                                """,
                                'test.yaml',
                                [{'a': 1, 'b': 2}]
                              ),
                              (#Test 2
                                """
                                version: 1.0
                                app: yamala
                                users:
                                    - charmander@poke.mon
                                    - squirtle@poke.mon
                                    - pikachu@poke.mon
                                """,
                                'test_2.yml',
                                [
                                    {
                                        'version': 1.0,
                                        'app': 'yamala',
                                        'users': [
                                                    'charmander@poke.mon',
                                                    'squirtle@poke.mon',
                                                    'pikachu@poke.mon'
                                                 ]
                                    }
                                ]
                              ),
                              (#Test 3
                                 dedent(
                                     """
                                     ---
                                     a: 1
                                     b: 2
                                     ...
                                     ---
                                     a: 5
                                     b: 6
                                     ...
                                     """
                                 ),
                                 "test_3.yaml",
                                 [
                                     {'a': 1, 'b': 2},
                                     {'a': 5, 'b': 6}
                                 ]
                              ),
                              (#Test 4
                                dedent(
                                    """
                                    version: '2.1'
                                    services:
                                        redis:
                                            image: 'redis:5.0.5'
                                            command: redis-server --requirepass redispass
                                    
                                        postgres:
                                            image: postgres:9.6
                                    """
                                ),
                                'test_4.yml',
                                [
                                    {
                                        'version': '2.1',
                                        'services': {
                                                        'redis': {
                                                                    'image': 'redis:5.0.5',
                                                                    'command': 'redis-server --requirepass redispass'
                                                                 },
                                                        'postgres': {
                                                                        'image': 'postgres:9.6'
                                                                    }
                                                    }
                                    }
                                ]
                              ),
                              (#Test 5
                                dedent(
                                    """
                                    a:
                                        b:
                                            c:
                                                - 1
                                                - 2
                                                - 3  
                                    """
                                ),
                                'test_5.yaml',
                                [
                                    {'a': {'b': {'c': [1, 2, 3]}}}
                                ]
                              )
                         ], ids=[
                                    'simple-case-1',
                                    'simple-list-1',
                                    'multi-docs-1',
                                    'mini-docker-compose-1',
                                    'prone-to-be-flattened-1'
                                ]

                         )
def test_pyyaml_content_retrieval(instantiate_pyyaml_reader, build_temp_file_factory, text, name, expected):
    path = build_temp_file_factory(text, name)
    content = instantiate_pyyaml_reader.load(path)
    assert isinstance(content, Iterable)
    assert content == expected


# #### Sad Path
@pytest.mark.parametrize(('filepath', 'output'),
                         [
                             (#Test 1
                                 '/home/path/file.xlsx', 'File extension must be .yaml or .yml'
                             ),
                             (#Test2
                                 '/home/path/file.yeml', 'File extension must be .yaml or .yml'
                             )
                         ], ids=[
                                    'excel_file-str',
                                    'yeml_extension'
                                ]
                         )
def test_file_ext(instantiate_pyyaml_reader, filepath, output):
    with pytest.raises(FileTypeError) as exp:
        instantiate_pyyaml_reader.load(filepath)

    assert exp.value.args[0] == output
