from dataclasses import dataclass
from typing import Any, List


@dataclass
class TableRow:
    current_time: str
    content: str
    content_trans: str
    editable: bool = True  # mặc định cho phép chỉnh sửa


class TableData:
    def __init__(self):
        self._rows: List[TableRow] = []
        self._column_names = ["Thời gian", "Nội dung", "Đã dịch"]

    def add_row(self, row: TableRow):
        self._rows.append(row)

    def remove_row(self, row_index: int):
        if 0 <= row_index < len(self._rows):
            del self._rows[row_index]

    def update_row(self, row_index: int, new_data: TableRow):
        if 0 <= row_index < len(self._rows):
            self._rows[row_index] = new_data

    def update_row_col(self, row_index: int, col_index: int, new_data: str):
        if 0 <= row_index < len(self._rows):
            if col_index == 0:
                self._rows[row_index].current_time = new_data
            elif col_index == 1:
                self._rows[row_index].content = new_data
            elif col_index == 2:
                self._rows[row_index].content_trans = new_data

    def get_row(self, row_index: int) -> TableRow:
        return self._rows[row_index]

    def get_all(self) -> List[TableRow]:
        return self._rows

    def row_count(self) -> int:
        return len(self._rows)

    def column_count(self) -> int:
        return len(self._column_names)  # id, content, content_trans, current_time

    def get_data(self, row: int, column: int) -> Any:
        if 0 <= row < self.row_count():
            r = self._rows[row]
            return [r.content, r.content_trans, r.current_time][column]
        return None

    def get_name_column(self) -> list[str]:
        return self._column_names
