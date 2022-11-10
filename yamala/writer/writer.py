"""
Module for Writer classes
"""
import abc
from pathlib import Path
from typing import Iterable, Iterator, Union, TypeVar

PathLikeObj = TypeVar('PathLikeObj', str, Path)


class AbstractWriter(abc.ABC):

    def __init__(self, folderpath: PathLikeObj, *args, **kwargs):
        self.folderpath = folderpath

    @abc.abstractmethod
    def process(self, input: Union[Iterable, Iterator]) -> None:
        """
        Method that receives a data structure and this used to populate an Excel Workbook
        """
        return NotImplemented()

    @abc.abstractmethod
    def save(self, filename: str) -> None:
        """
        filename will not require extension, since any saved must be .xlsx
        """
        return NotImplemented()


class OpenxlpyWriter(AbstractWriter):

    def process(self, input: Union[Iterable, Iterator]) -> None:
        pass

    def save(self, filename: str) -> None:
        pass
