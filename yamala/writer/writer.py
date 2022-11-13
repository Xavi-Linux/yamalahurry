"""
Module for Writer classes
"""
import abc
from openpyxl.workbook.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from pathlib import Path
from typing import Dict, Iterable, Iterator, List, Union, Tuple, TypeVar

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
    def process(self, inputs: Union[Iterable, Iterator]) -> None:
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

    def __init__(self, folderpath: PathLikeObj):
        AbstractWriter.__init__(self, folderpath)
        self.workbook: Workbook = Workbook()
        self._input: Union[None, Dict[str, Dict[str, Union[Dict, List]]]] = None

    def process(self, inputs: Dict[str, Dict[str, Union[Dict, List]]]) -> None:
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
        self._input = inputs

        self._validate_input()

        #By default, a workbook instance holds a worksheet called 'Sheet'
        self.workbook.remove(self.workbook.worksheets[0])
        for index, sheet in enumerate(self._input):
            clean_name: str = self._clear_sheet_name(sheet)
            #A sheet's name have a maximum of 31 characters:
            unique_name: str = self._generate_worksheet_name(clean_name[-31:], self.workbook.sheetnames)
            current_sheet: Worksheet = self.workbook.create_sheet(title=unique_name, index=index)

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

    @staticmethod
    def _generate_worksheet_name(name: str, current_sheets: List[str], recursion_level: int = 1) -> str:
        """
        - Avoid potential name duplications:
            if 'sheet' already exists, 'sheet' -> 'sheet_1'
            if 'sheet_1' already exists, 'sheet_1' -> 'sheet_2'
        - Proper name is found recursively
        """
        if name.lower() not in current_sheets:
            return name.lower()

        else:
            return OpenxlpyWriter._generate_worksheet_name(
                                        name.lower() + '_' + str(recursion_level),
                                        current_sheets,
                                        recursion_level + 1
            )

    @staticmethod
    def _clear_sheet_name(name: str) -> str:
        forbidden_symbols: Tuple = ('\\', '/', '*', '[', ']', ':', '?')
        replacer: str = '_'
        for symbol in forbidden_symbols:
            name = name.replace(symbol, replacer)

        return name
