from PyQt6.QtCore import QObject, pyqtSignal


class Controller(QObject):
    update_view_signal = pyqtSignal()

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

    def ocr_image(self):
        # image_path = self.view.get_image_path()
        pass
