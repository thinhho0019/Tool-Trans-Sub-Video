from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from styles.constranst import BUTTON_STYLESHEET, HOVER_BUTTON_STYLESHEET
from view.components.video_player import VideoSlider

DIRECT_VIDEO = (
    r"C:\Users\ADMIN\Downloads\518126526_1284718069929382_2791823199093414151_n.jpg"
)
ICON_PLAY = r"C:\Users\ADMIN\Desktop\tool-video-sub\public\icon\play-button.png"
ICON_STOP_VIDEO = r"C:\Users\ADMIN\Desktop\tool-video-sub\public\icon\stop-button.png"


class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle("Tool Video Sub")
        layout = QVBoxLayout()
        layout.addLayout(self.ui_config_direct_video())
        layout.addLayout(self.ui_config_video())
        layout.addLayout(self.ui_config_subtitle())
        self.setLayout(layout)

    def ui_config_video(self) -> QVBoxLayout:
        qv_layout = QVBoxLayout()

        self.video_label = QLabel("Video Player Placeholder")

        pixmap = QPixmap(DIRECT_VIDEO)
        pixmap = pixmap.scaledToWidth(300)  # Adjust width as needed
        self.video_label.setPixmap(pixmap)
        self.video_button = QPushButton("  Play Video")
        self.video_button.setIcon(QIcon(ICON_PLAY))
        self.video_button.setMaximumWidth(100)
        self.video_button_stop = QPushButton("  Stop Video")
        self.video_button_stop.setIcon(QIcon(ICON_STOP_VIDEO))
        self.video_button_stop.setMaximumWidth(100)
        self.range_video = QLabel("00:00")
        self.slider_video = VideoSlider()
        self.slider_video.sliderMovedManually.connect(self.listen_duration_slider)

        qv_layout.addWidget(self.video_label, alignment=Qt.AlignmentFlag.AlignCenter)
        qv_layout.addLayout(
            self.create_ui_hbox(
                [{"widget": self.video_button}, {"widget": self.video_button_stop}],
                align=Qt.AlignmentFlag.AlignCenter,
            )
        )
        qv_layout.addLayout(
            self.create_ui_hbox(
                [
                    {"widget": self.slider_video, "strech": 1},
                    {"widget": self.range_video, "strech": 1},
                ],
                align=Qt.AlignmentFlag.AlignCenter,
            )
        )
        return qv_layout

    def listen_duration_slider(duration):
        # self.range_video.setText("12:00")
        pass

    def ui_config_subtitle(self) -> QVBoxLayout:
        qv_layout = QVBoxLayout()
        self.subtitle_label = QLabel("Subtitle Placeholder")
        self.subtitle_button = QPushButton("Load Subtitle")
        qv_layout.addWidget(self.subtitle_label)
        qv_layout.addWidget(self.subtitle_button)
        return qv_layout

    def ui_config_direct_video(self) -> QVBoxLayout:
        qv_layout = QVBoxLayout()
        self.direct_video_label = QLabel("Enter button choose direct video")
        self.direct_video_label.setStyleSheet(
            "border: 1px solid black;border-radius:6px;border-color:white"
        )
        self.direct_video_button = QPushButton("Load Direct Video")
        self.direct_video_button.setStyleSheet(
            BUTTON_STYLESHEET + HOVER_BUTTON_STYLESHEET
        )
        qv_layout.addLayout(
            self.create_ui_hbox(
                [
                    {"widget": self.direct_video_label, "strech": 8},
                    {"widget": self.direct_video_button, "strech": 2},
                ]
            ),
        )
        return qv_layout

    def create_ui_hbox(self, widget: list[dict], align=None) -> QHBoxLayout:
        hbox = QHBoxLayout()
        for item in widget:
            widget_item = item.get("widget")
            strech = item.get("strech", 1)
            if align is not None:
                hbox.addWidget(widget_item, stretch=strech, alignment=align)
                return
            hbox.addWidget(widget_item, stretch=strech)
