from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QDialog, QLabel, QProgressBar, QPushButton, QVBoxLayout


class LoadingDialog(QDialog):
    cancel_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Đang tải...")
        self.setModal(True)
        self.setWindowFlags(
            self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint
        )
        self.resize(300, 120)

        self.layout = QVBoxLayout(self)
        self.label = QLabel("Đang tải dữ liệu...", self)
        self.label_infor = QLabel("...")
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 100)
        self.cancel_btn = QPushButton("Hủy", self)
        self.cancel_btn.clicked.connect(self.cancel_signal.emit)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label_infor)
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.cancel_btn)

    def set_status(self, text: str):
        self.label.setText(text)

    def set_progress(self, value: int):
        self.progress.setValue(value)

    def closeEvent(self, event: QCloseEvent):
        print("Dialog đã bị đóng")
        self.cancel_signal.emit()
        event.accept()  # hoặc event.ignore() nếu muốn chặn đóng
