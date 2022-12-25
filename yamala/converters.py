"""
Classes that transform outputs of a reader into inputs of a writer
"""

import abc
from pathlib import Path
from typing import Dict, List
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
    def read(self) -> None:
        pass

    @abc.abstractmethod
    def transform(self) -> None:
        pass

    @abc.abstractmethod
    def write(self) -> None:
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
        self._files: List[str] = files
        self._are_files: bool = True
        self._converted_files: List[Path] = []

        self._inspect_files()

        self.destination: Path = destination
        self.recursive: bool = recursive
        self.processed_files: int = 0
        self.raw_contents: List[Dict] = []
        self.reader = PyYamlReader()
        self.writer = OpenxlpyWriter(Path.cwd())

    @property
    def files(self):
        return self._files

    @files.setter
    def files(self, values: List[str]):
        self._converted_files = []
        self._files = values
        self._inspect_files()

    def read(self) -> None:
        for file in self._converted_files:
            if self._are_files:
                self._read_file(file)
                self.processed_files += 1

            else:
                self._read_folder(file)

    def transform(self) -> None:
        pass

    def write(self) -> None:
        pass

    def _inspect_files(self) -> None:
        for file in self._files:
            self._converted_files.append(Path(file))
            if not self._converted_files[-1].exists():
                raise FileNotFoundError(f'{file} does not exist')

        self._are_files = all(map(Path.is_file, self._converted_files))

    def _read_file(self, file: Path) -> None:
        documents: List = self.reader.load(file)
        for document in documents:
            if isinstance(document, Dict):
                self.raw_contents.append(document)

            else:
                self.raw_contents.append({document: None})

    def _read_folder(self, folder: Path):
        for file in folder.iterdir():
            if file.is_dir() and self.recursive:
                self._read_folder(file)

            else:
                if file.suffix == '.yaml' or file.suffix == '.yml':
                    self._read_file(file)
                    self.processed_files += 1
