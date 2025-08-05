from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QSlider, QStyle, QStyleOptionSlider


class VideoSlider(QSlider):
    sliderMovedManually = pyqtSignal(int)

    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.setRange(0, 0)
        self.sliderMoved.connect(self.on_slider_moved)

    def on_slider_moved(self, position):
        print(position)
        self.sliderMovedManually.emit(position)

    def update_position(self, position: int):
        self.setValue(position)

    def update_duration(self, duration: int):
        self.setRange(0, duration)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            option = QStyleOptionSlider()
            self.initStyleOption(option)
            style = self.style()
            groove_rect = style.subControlRect(
                QStyle.ComplexControl.CC_Slider,
                option,
                QStyle.SubControl.SC_SliderGroove,
                self,
            )
            handle_rect = style.subControlRect(
                QStyle.ComplexControl.CC_Slider,
                option,
                QStyle.SubControl.SC_SliderHandle,
                self,
            )

            if self.orientation() == Qt.Orientation.Horizontal:
                slider_length = handle_rect.width()
                slider_min = groove_rect.x()
                slider_max = groove_rect.right() - slider_length + 1
                pos = event.position().x()
            else:
                slider_length = handle_rect.height()
                slider_min = groove_rect.y()
                slider_max = groove_rect.bottom() - slider_length + 1
                pos = event.position().y()

            new_val = QStyle.sliderValueFromPosition(
                self.minimum(),
                self.maximum(),
                int(pos - slider_min),
                slider_max - slider_min,
                upsideDown=False,
            )
            self.setValue(new_val)
            self.sliderMovedManually.emit(new_val)
            event.accept()
        super().mousePressEvent(event)
