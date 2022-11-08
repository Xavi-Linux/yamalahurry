"""
Yaml parser
"""
from typing import Dict, Union, TypeVar, Iterable, Iterator
from pathlib import Path
from yaml import load_all
import abc

PathLikeObj = TypeVar('PathLikeObj', str, Path)


class FileTypeError(Exception):

    def __init__(self):
        Exception.__init__(self, 'File extension must be .yaml or .yml')


class AbstractReader(abc.ABC):

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    @abc.abstractmethod
    def load(self, filepath: PathLikeObj) -> Union[Iterable, Iterator]:
        return NotImplemented

    @staticmethod
    def _validate_extension(filepath: PathLikeObj) -> None:
        if not (filepath[-4:]=='.yml' or filepath[-5:]=='.yaml'):
            raise FileTypeError()


class PyYamlReader(AbstractReader):

    def load(self, filepath: PathLikeObj) -> Iterator:
        self._validate_extension(filepath)
        return {}

