"""
Yaml readers: interfaces + implementations
"""
from typing import Dict, List, Union, TypeVar, Iterable, Generator
from pathlib import Path
import abc
import yaml

PathLikeObj = TypeVar('PathLikeObj', str, Path)


class FileTypeError(Exception):
    """
    Instantiate this class to raise when the supplied files is not yaml
    """
    def __init__(self):
        Exception.__init__(self, 'File extension must be .yaml or .yml')


class AbstractReader(abc.ABC):
    """
    Abstract class to ingrain an interface in any future yaml reader
    """
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    @abc.abstractmethod
    def load(self, filepath: PathLikeObj) -> Iterable:
        return NotImplemented

    @staticmethod
    def _validate_extension(filepath: PathLikeObj) -> None:
        filepath_str: str
        if isinstance(filepath, Path):
            filepath_str = filepath.suffix
        else:
            filepath_str = filepath

        if not (filepath_str[-4:]=='.yml' or filepath_str[-5:]=='.yaml'):
            raise FileTypeError()


class PyYamlReader(AbstractReader):
    """
    Implement a reader using third-party library pyyaml
    """
    def load(self, filepath: PathLikeObj) -> List:
        self._validate_extension(filepath)
        files: List = []
        with open(filepath, 'r') as f:
            content: Generator = yaml.safe_load_all(f)
            for file in content:
                files.append(file)

        return files



