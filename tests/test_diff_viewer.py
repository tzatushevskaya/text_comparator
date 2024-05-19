import sys

import pytest
from PySide6 import QtGui, QtWidgets
from PySide6.QtWidgets import QApplication

from text_comparator.diff_viewer import DiffViewer, MainWindow


def test_get_diff_summary():
    if not QtWidgets.QApplication.instance():
        APP = QtWidgets.QApplication([])
    # Given
    file1_content = "def foo():\n    print('Hello, World!')\n"
    file2_content = "def foo():\n    print('Hello, Python!')\n    print('New line')\n"

    # When
    diff_viewer = DiffViewer(file1_content=file1_content, file2_content=file2_content)
    summary = diff_viewer.get_diff_summary()

    # Then
    assert summary == "2 additions, 1 removals"
