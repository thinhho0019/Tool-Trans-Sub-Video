from dataclasses import asdict

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem


class TableViewSub(QTableWidget):
    cellValueChanged = pyqtSignal(int, int, str)  # row, column, new_value

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(500)
        self.setColumnCount(0)
        self.setRowCount(0)
        self.setEditTriggers(
            QTableWidget.EditTrigger.DoubleClicked
            | QTableWidget.EditTrigger.SelectedClicked
        )
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.cellChanged.connect(self.on_cell_changed)
        self._data = []

    def show_data(self, data):
        self.clear()
        self.setColumnCount(data.column_count())
        self.setHorizontalHeaderLabels(data.get_name_column())
        self.setRowCount(data.row_count())
        self._data = data.get_all()  # Optional: store data for reuse
        for index, value in enumerate(self._data):
            for col_idx, (k, v) in enumerate(asdict(value).items()):
                item = QTableWidgetItem(str(v))
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
                self.setItem(index, col_idx, item)

    def on_cell_changed(self, row, column):
        item = self.item(row, column)
        if item:
            new_value = item.text()
            self.cellValueChanged.emit(row, column, new_value)
