from PyQt6.QtWidgets import QApplication, QMainWindow
import sys
from view.view import MainView
from controller.controller import Controller

def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    view = MainView()
    model = None  # Placeholder for the model, to be defined later
    controller = Controller(model,view)

    main_window.setCentralWidget(view)
    main_window.setWindowTitle("PyQt6 MVC Application")
    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()