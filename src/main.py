import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow

from controller.controller import Controller
from model.table_data import TableData
from services.share_memories.ocr_pool import OcrPool
from view.view import MainView


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("../public/icon/icon-main.ico"))
    main_window = QMainWindow()
    # singleton services
    model = TableData()
    view = MainView()  # Placeholder for the model, to be defined later
    pool = OcrPool()
    pool.init_pool()
    controller = Controller(model, view, pool)  # noqa

    main_window.setCentralWidget(view)
    main_window.setWindowTitle("Tool Sub Translate Video")
    main_window.resize(1300, 600)

    # Center the window on the screen
    screen_geometry = app.primaryScreen().availableGeometry()
    x = (screen_geometry.width() - main_window.width()) // 2
    y = (screen_geometry.height() - main_window.height()) // 2
    main_window.move(x, y)

    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
