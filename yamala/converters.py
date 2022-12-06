"""
Classes that transform outputs of a reader into inputs of a writer
"""

import abc
from pathlib import Path
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
