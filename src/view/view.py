from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLayout,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.styles.constranst import BUTTON_STYLESHEET, HOVER_BUTTON_STYLESHEET
from src.view.components.graphic_video import GraphicVideo
from src.view.components.table_view_sub import TableViewSub
from src.view.components.video_player import VideoSlider

ICON_PLAY = (
    r"C:\Users\ADMIN\Desktop\tool-video-sub\public\icon\play-button-arrowhead.png"
)
ICON_STOP_VIDEO = r"C:\Users\ADMIN\Desktop\tool-video-sub\public\icon\stop-button.png"


class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self) -> None:
        self.setWindowTitle("Tool Video Sub")
        layout = QVBoxLayout()
        layout.addLayout(
            self.create_ui_hbox(
                [
                    {
                        "widget": self.create_ui_vbox(
                            [
                                {"widget": self.ui_config_direct_video()},
                                {"widget": self.ui_config_video()},
                                {"widget": self.ui_show_infor_video()},
                            ]
                        )
                    },
                    {"widget": self.ui_config_sub()},
                ]
            )
        )
        self.setLayout(layout)

    def ui_config_video(self) -> QVBoxLayout:
        qv_layout = QVBoxLayout()
        self.video_label = GraphicVideo()
        self.video_button = QPushButton("  Play Video")
        self.video_button.setIcon(QIcon(ICON_PLAY))
        self.video_button.setMaximumWidth(120)
        self.video_button.setMinimumHeight(30)
        self.video_button_stop = QPushButton("  Stop Video")
        self.video_button_stop.setIcon(QIcon(ICON_STOP_VIDEO))
        self.video_button_stop.setMaximumWidth(100)
        self.video_button_stop.setMinimumHeight(30)
        self.range_video = QLabel("00:00")
        self.slider_video = VideoSlider()

        qv_layout.addWidget(self.video_label, alignment=Qt.AlignmentFlag.AlignCenter)
        slider_layout = self.create_ui_hbox(
            [
                {"widget": self.slider_video, "strech": 10},
                {"widget": self.range_video, "strech": 0},
            ]
        )

        qv_layout.addLayout(slider_layout)
        qv_layout.addLayout(
            self.create_ui_hbox(
                [
                    {"widget": self.video_button, "align": Qt.AlignmentFlag.AlignRight},
                    {
                        "widget": self.video_button_stop,
                        "align": Qt.AlignmentFlag.AlignLeft,
                    },
                ]
            )
        )
        qv_layout.setAlignment(slider_layout, Qt.AlignmentFlag.AlignCenter)

        return qv_layout

    def ui_show_infor_video(self):
        qvbox = QVBoxLayout()
        self.textedit_infor = QTextEdit()
        self.textedit_infor.setReadOnly(True)

        qvbox.addWidget(self.textedit_infor)
        return qvbox

    def ui_config_sub(self):
        qv_layout = QVBoxLayout()
        self.table_view = TableViewSub()
        qv_layout.addWidget(self.table_view)
        return qv_layout

    def ui_config_direct_video(self) -> QVBoxLayout:
        qv_layout = QVBoxLayout()
        self.direct_video_label = QLabel("Enter button choose direct video")
        self.direct_video_label.setStyleSheet(
            "border: 1px solid black;border-radius:6px;border-color:white"
        )
        self.btn_export_sub_video = QPushButton("Export sub video ->")
        self.btn_export_sub_video.setStyleSheet(
            BUTTON_STYLESHEET + HOVER_BUTTON_STYLESHEET
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
                    {"widget": self.btn_export_sub_video, "strech": 2},
                ]
            ),
        )
        return qv_layout

    def create_ui_hbox(self, widget: list[dict]) -> QHBoxLayout:
        hbox = QHBoxLayout()
        for item in widget:
            widget_item = item.get("widget")
            strech = item.get("strech", 1)
            item_align = item.get("align", None)

            if isinstance(widget_item, QLayout):
                if item_align is not None:
                    hbox.addLayout(widget_item, stretch=strech)
                else:
                    hbox.addLayout(widget_item, stretch=strech)
            else:
                if item_align is not None:
                    hbox.addWidget(widget_item, stretch=strech, alignment=item_align)
                else:
                    hbox.addWidget(widget_item, stretch=strech)
        return hbox

    def create_ui_vbox(self, widget: list[dict]) -> QVBoxLayout:
        vbox = QVBoxLayout()
        for item in widget:
            widget_item = item.get("widget")
            strech = item.get("strech", 1)
            item_align = item.get("align", None)

            if isinstance(widget_item, QLayout):
                if item_align is not None:
                    vbox.addLayout(widget_item, stretch=strech)
                else:
                    vbox.addLayout(widget_item, stretch=strech)
            else:
                if item_align is not None:
                    vbox.addWidget(widget_item, stretch=strech, alignment=item_align)
                else:
                    vbox.addWidget(widget_item, stretch=strech)
        return vbox
