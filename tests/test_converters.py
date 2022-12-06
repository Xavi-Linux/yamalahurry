"""
Tests for the converter class
"""

import pytest

from pathlib import Path
from typing import Dict, List
from yamalahurry.yamala.converters import PyYamlToOpenpyxlConverter


def test_converter_instantiation():
    inputs: Dict = {
        'files': ['folder1', 'folder2'],
        'destination': Path('/folder/'),
        'recursive': False
    }
    converter = PyYamlToOpenpyxlConverter(**inputs)
    assert hasattr(converter, 'writer')
    assert hasattr(converter, 'reader')
    assert hasattr(converter, 'read')
    assert hasattr(converter, 'transform')
    assert hasattr(converter, 'write')
    assert hasattr(converter, 'files') and isinstance(converter.files, List)
    assert hasattr(converter, 'destination') and isinstance(converter.destination, Path)
    assert hasattr(converter, 'recursive') and isinstance(converter.recursive, bool)
