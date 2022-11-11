"""
Module for Writer classes
"""
import abc
from openpyxl.workbook.workbook import Workbook
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Union, TypeVar

PathLikeObj = TypeVar('PathLikeObj', str, Path)


class WrongInputStructure(Exception):

    def __init__(self, message: str):
        Exception.__init__(self, message)


class AbstractWriter(abc.ABC):

    def __init__(self, folderpath: PathLikeObj, *args, **kwargs):
        if isinstance(folderpath, str):
            folderpath = Path(folderpath)

        self.folderpath: Path = folderpath

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

    def __init__(self,folderpath: PathLikeObj, *args, **kwargs):
        AbstractWriter.__init__(self, folderpath)
        self.workbook = Workbook()
        self._input = None

    def process(self, input: Dict[str, Dict[str, Union[Dict, List]]]) -> None:
        """
        input must have the following structure:

            {
                'sheet1_name: {
                        'rows': ['row1_text', 'row2_text' ...],
                        'columns: {
                                'column1_header': [row1_col1_value, row2_col1_value, ...],
                                'column2_header: ...
                        }
                },
                'sheet2_name: ...
            }

        """
        self._input = input

        self._validate_input()

    def save(self, filename: str) -> None:
        pass

    def _validate_input(self) -> None:
        if isinstance(self._input, Dict):
            if len(self._input) > 0:
                if all(
                        map(
                            lambda v: isinstance(v, Dict),
                            self._input.values()
                        )
                ):
                    all_sheets_validated: bool = False
                    for sheet in self._input:
                        all_sheets_validated = False
                        try:
                            rows = self._input[sheet]['rows']
                            columns = self._input[sheet]['columns']
                            if isinstance(rows, List) and isinstance(columns, Dict):
                                rows_len: int = len(rows)
                                if all(
                                        map(
                                            lambda v: isinstance(v, List) and len(v) == rows_len,
                                            columns.values()
                                        )
                                ):
                                    all_sheets_validated = True

                        except KeyError:
                            raise WrongInputStructure(self.process.__doc__)

                    if all_sheets_validated:
                        return None

        raise WrongInputStructure(self.process.__doc__)
