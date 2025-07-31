from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QSlider


class VideoSlider(QSlider):
    sliderMovedManually = pyqtSignal(int)

    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.setRange(0, 0)
        self.sliderMoved.connect(self.on_slider_moved)

    def on_slider_moved(self, position):
        self.sliderMovedManually.emit(position)

    def update_position(self, position: int):
        self.setValue(position)

    def update_duration(self, duration: int):
        self.setRange(0, duration)
