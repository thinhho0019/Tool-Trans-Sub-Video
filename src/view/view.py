from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('PyQt6 MVC Application')
        layout = QVBoxLayout()

        self.label = QLabel('Welcome to the PyQt6 MVC App')
        layout.addWidget(self.label)

        self.button = QPushButton('Click Me')
        layout.addWidget(self.button)

        self.setLayout(layout)