import difflib
from pathlib import Path

from PySide6.QtCore import QSize, QRect, Qt
from PySide6.QtGui import QPainter, QColor, QTextFormat, QSyntaxHighlighter
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QMainWindow,
    QPlainTextEdit,
    QTextEdit,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QStackedWidget,
)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)
        self.update_line_number_area_width(0)
        self.highlight_current_line()

        # Set default text color
        self.setStyleSheet("color: rgb(0, 255, 255);")

    def line_number_area_width(self):
        digits = 1
        max_line = max(1, self.blockCount())
        while max_line >= 10:
            max_line //= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance("9") * digits
        return space

    def update_line_number_area_width(self, _):
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(
                0, rect.y(), self.lineNumberArea.width(), rect.height()
            )

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(
            QRect(cr.left(), cr.top(), self.line_number_area_width(), cr.height())
        )

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.GlobalColor.lightGray)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.GlobalColor.black)
                painter.drawText(
                    0,
                    top,
                    self.lineNumberArea.width(),
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    number,
                )

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlight_current_line(self):
        extra_selections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            line_color = QColor(Qt.GlobalColor.yellow).lighter(160)
            selection.cursor.blockFormat().setBackground(line_color)
            selection.cursor.blockFormat().setProperty(
                QTextFormat.Property.FullWidthSelection, True
            )
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)


class DiffHighlighter(QSyntaxHighlighter):
    def __init__(self, document, diff_lines):
        super().__init__(document)
        self.diff_lines = diff_lines

    def highlightBlock(self, text):
        for line in self.diff_lines:
            if text in line:
                if line.startswith("+"):
                    self.setFormat(
                        0, len(text), QColor(138, 255, 0)
                    )  # acid green background
                elif line.startswith("-"):
                    self.setFormat(
                        0, len(text), QColor(255, 20, 147)
                    )  # acid pink background
                break


class DiffViewer(QWidget):
    def __init__(self, file1_content, file2_content):
        super().__init__()
        layout = QHBoxLayout(self)
        self.editor1 = CodeEditor()
        self.editor2 = CodeEditor()
        layout.addWidget(self.editor1)
        layout.addWidget(self.editor2)

        # Split files into lines
        file1_lines = file1_content.splitlines(keepends=True)
        file2_lines = file2_content.splitlines(keepends=True)

        # Compute the diff
        d = difflib.Differ()
        diff = list(d.compare(file1_lines, file2_lines))

        # Count additions and removals
        self.additions = sum(1 for line in diff if line.startswith("+"))
        self.removals = sum(1 for line in diff if line.startswith("-"))

        # Apply the diff highlighter
        DiffHighlighter(self.editor1.document(), diff)
        DiffHighlighter(self.editor2.document(), diff)

        # Set text in editors
        self.editor1.setPlainText("".join(file1_lines))
        self.editor2.setPlainText("".join(file2_lines))

    def get_diff_summary(self):
        if self.additions == 0 and self.removals == 0:
            return "No differences"
        return f"{self.additions} additions, {self.removals} removals"


class FileSelectionPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.button1 = QPushButton("Select File 1")
        self.button2 = QPushButton("Select File 2")
        self.compare_button = QPushButton("Compare")
        self.compare_button.setEnabled(False)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.compare_button)


class ComparisonPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.diff_viewer = None

    def update_comparison(self, file1_content, file2_content):
        # self.diff_viewer.update_comparison(file1_content, file2_content)
        self.diff_viewer = DiffViewer(
            file1_content=file1_content,
            file2_content=file2_content,
        )
        self.layout.addWidget(self.diff_viewer)

        # Set the background color of the entire window
        self.setStyleSheet("background-color: black;")

        # Access the main window to update its properties
        main_window = self.window()
        if isinstance(main_window, QMainWindow):
            # Set window title with diff summary
            # self.setWindowTitle("Diff Viewer")
            main_window.setGeometry(100, 100, 1200, 800)
            main_window.setWindowTitle(
                f"Diff Viewer - {self.diff_viewer.get_diff_summary()}"
            )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Diff Viewer")
        self.setGeometry(100, 100, 400, 200)
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.file_selection_page = FileSelectionPage()
        self.comparison_page = ComparisonPage()

        self.stacked_widget.addWidget(self.file_selection_page)
        self.stacked_widget.addWidget(self.comparison_page)

        # Connect signals to select files
        self.file_selection_page.button1.clicked.connect(self.select_file1)
        self.file_selection_page.button2.clicked.connect(self.select_file2)
        self.file_selection_page.compare_button.clicked.connect(
            self.show_comparison_page
        )

        self.file1_content = ""
        self.file2_content = ""

    def select_file1(self):
        file_path = self.get_file_path()
        if file_path:
            self.file_selection_page.button1.setText(file_path)
            with open(file_path, "r") as file:
                self.file1_content = file.read()
            self.check_files_selected()

    def select_file2(self):
        file_path = self.get_file_path()
        if file_path:
            self.file_selection_page.button2.setText(file_path)
            with open(file_path, "r") as file:
                self.file2_content = file.read()
            self.check_files_selected()

    def check_files_selected(self):
        if self.file1_content and self.file2_content:
            self.file_selection_page.compare_button.setEnabled(True)

    def show_comparison_page(self):
        if self.file1_content and self.file2_content:
            self.comparison_page.update_comparison(
                self.file1_content, self.file2_content
            )
            self.stacked_widget.setCurrentWidget(self.comparison_page)

    def get_file_path(self):
        # Set the initial directory here
        initial_dir = Path("./tests/code_samples")

        # Open file dialog with initial directory to select a file and return its path
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select File", str(initial_dir), "All Files (*)"
        )
        return file_path
