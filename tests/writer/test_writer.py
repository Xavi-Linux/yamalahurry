"""
Test file for the Writer Classes
"""
import pytest

from yamalahurry.yamala.writer import OpenxlpyWriter


@pytest.fixture
def make_folder(tmp_path):
    folder = tmp_path / 'tests'
    return folder.mkdir()


def test_call(make_folder):
    writer = OpenxlpyWriter(make_folder)

