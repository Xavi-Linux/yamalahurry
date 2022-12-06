"""
Classes that transform outputs of a reader into inputs of a writer
"""

import abc
from pathlib import Path
from typing import List
from .reader import AbstractReader, PyYamlReader
from .writer import AbstractWriter, OpenxlpyWriter


class AbstractConverter(abc.ABC):
    """
    Abstract class to ingrain some interface in any implemented converter
    """

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        self.reader: AbstractReader = AbstractReader()
        self.writer: AbstractWriter = AbstractWriter(Path.cwd())

    @abc.abstractmethod
    def read(self):
        pass

    @abc.abstractmethod
    def transform(self):
        pass

    @abc.abstractmethod
    def write(self):
        pass

    def execute(self):
        self.read()
        self.transform()
        self.write()


class PyYamlToOpenpyxlConverter(AbstractConverter):
    """
    Class that uses third-party yaml handler pyyaml and third-party Excel handler
    Openpyxl.
    """
    def __init__(self, files: List[str], destination: Path, recursive: bool):
        self.files: List[str] = files
        self.destination: Path = destination
        self.recursive: bool = recursive
        self.reader = PyYamlReader()
        self.writer = OpenxlpyWriter(Path.cwd())

    def read(self):
        pass

    def transform(self):
        pass

    def write(self):
        pass
