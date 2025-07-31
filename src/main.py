import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow

from controller.controller import Controller
from view.view import MainView


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./public/icon/icon-main.ico"))
    main_window = QMainWindow()
    view = MainView()
    model = None  # Placeholder for the model, to be defined later
    Controller(model, view)

    main_window.setCentralWidget(view)
    main_window.setWindowTitle("PyQt6 MVC Application")
    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
