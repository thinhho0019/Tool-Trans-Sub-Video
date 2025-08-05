import cv2
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFileDialog

from src.model.table_data import TableData, TableRow
from src.multithreads.thread_get_sub_video import ThreadGetSubVideo
from src.multithreads.thread_loading_video import ThreadLoadingVideo
from src.utils.message_box import show_message
from src.view.components.loading_dialog import LoadingDialog

DATA_SYSTEM_INFOR_VIDEO = {
    "label": "THÔNG TIN VIDEO",
    "fps": "",
    "resolution": "",
    "duration": "",
    "qrect": "",
    "direct_video": "",
}


class Controller(QObject):
    update_view_signal = pyqtSignal()

    def __init__(self, model: TableData, view, pool):
        super().__init__()
        self.model = model
        self.view = view
        self.pool = pool
        # listen button connect
        self.view.direct_video_button.clicked.connect(self.load_video_for_path)
        self.view.slider_video.sliderMovedManually.connect(self.listen_duration_slider)
        self.view.video_button_stop.clicked.connect(self.stop_video)
        self.view.video_button.clicked.connect(self.continue_video)
        self.view.video_label.box_items_signal.connect(self.update_infor_qrect)
        self.view.btn_export_sub_video.clicked.connect(self.button_exec_video_get_sub)
        self.view.table_view.cellValueChanged.connect(self.on_changed_value_table)
        self.qrect_box = None
        self.add_data_to_table()
        self.show_textedit_infor()

    def update_infor_qrect(self, rect):
        scene_rect = rect.rect()
        self.qrect_box = scene_rect
        rect_str = (
            f"x={scene_rect.x()}, y={scene_rect.y()}, "
            f"width={scene_rect.width()}, height={scene_rect.height()}"
        )
        DATA_SYSTEM_INFOR_VIDEO["qrect"] = rect_str
        self.show_textedit_infor()

    def add_data_to_table(self):
        self.view.table_view.show_data(self.model)

    def ocr_image(self):
        # image_path = self.view.get_image_path()
        pass

    def stop_video(self):
        if self.thread is not None:
            self.thread.pause_video()

    def continue_video(self):
        if self.thread is not None:
            self.thread.continue_video()

    def listen_duration_slider(self, duration):
        # self.range_video.setText("12:00")

        if self.thread is not None:
            self.thread.seek(duration)
        pass

    def button_exec_video_get_sub(self):
        path_video = self.view.direct_video_label.text()
        if path_video is None or path_video == "Enter button choose direct video":
            show_message(self.view, "Thông báo", "Vui lòng chọn đường dẫn video")
            return
        if self.qrect_box is None:
            show_message(
                self.view,
                "Thông báo",
                "Vui lòng vẽ vùng box chữ trên video để tool nhận dạng.",
            )
            return
        self.thread_exec_get_sub = ThreadGetSubVideo(
            path_video=path_video, qrect=self.qrect_box, pool=self.pool
        )
        self.thread_exec_get_sub.show_control.connect(self.show_notify_loading)
        self.thread_exec_get_sub.sum_progress.connect(self.show_sum_progress)
        self.thread_exec_get_sub.number_progress.connect(self.show_number_progress)
        self.thread_exec_get_sub.message_progress.connect(self.show_mesage_progress)
        self.thread_exec_get_sub.final_value.connect(self.show_final_value)
        self.thread_exec_get_sub.finished.connect(self.finish_thread_get_sub)
        self.thread_exec_get_sub.start()

    def set_current_duration(self, duration):
        self.view.slider_video.update_position(duration)
        self.view.range_video.setText(self.get_show_minus(duration))
        pass

    def set_data_infor(self, data):
        if "fps" in data:
            DATA_SYSTEM_INFOR_VIDEO["fps"] = data["fps"]
        if "resolution" in data:
            DATA_SYSTEM_INFOR_VIDEO["resolution"] = data["resolution"]
        if "duration" in data:
            DATA_SYSTEM_INFOR_VIDEO["duration"] = data["duration"]
        if "direct_video" in data:
            DATA_SYSTEM_INFOR_VIDEO["direct_video"] = data["direct_video"]
        self.show_textedit_infor()

    def set_range_video(self, duration):
        self.view.slider_video.setRange(0, duration)
        self.view.range_video.setText(self.get_show_minus(duration))

    def load_video_for_path(self):
        try:
            print(self.view.direct_video_label.text())
            file_path, _ = QFileDialog.getOpenFileName(
                self.view,
                "Chọn tệp video",
                "",
                "Video Files (*.mp4 *.avi *.mov *.mkv);;All Files (*)",
            )
            if file_path:
                self.thread = ThreadLoadingVideo(file_path)
                self.thread.frame_signal.connect(self.show_frame)
                self.thread.range_video.connect(self.set_range_video)
                self.thread.current_duration.connect(self.set_current_duration)
                self.thread.data_infor.connect(self.set_data_infor)
                self.view.direct_video_label.setText(file_path)
                self.thread.start()
        except Exception as ex:
            print(ex)
            show_message(f"Load video thất bại -> {str(ex)}")

    def show_frame(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        from PyQt6.QtGui import QImage, QPixmap

        qimg = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

        pixmap = QPixmap.fromImage(qimg)
        self.view.video_label.show_frame(pixmap)

    def get_show_minus(self, duration) -> str:
        minutes = f"{int(duration) // 60:02}"
        seconds = f"{int(duration) % 60:02}"
        duration_str = f"{minutes}:{seconds}"
        return duration_str

    def show_textedit_infor(self):
        self.view.textedit_infor.clear()
        # Đặt font mono để các chữ thẳng hàng
        mono_font = QFont("Courier New")  # hoặc "Consolas", "Monospace"
        mono_font.setStyleHint(QFont.StyleHint.Courier)
        self.view.textedit_infor.setFont(mono_font)

        self.view.textedit_infor.setMinimumHeight(100)
        # Tìm chiều dài key dài nhất để căn hàng
        max_key_length = max(len(key) for key in DATA_SYSTEM_INFOR_VIDEO.keys())

        # Dùng f-string để căn trái key và đặt dấu `:` thẳng hàng
        for key, value in DATA_SYSTEM_INFOR_VIDEO.items():
            line = f"{key.upper():<{max_key_length}} : {value}"
            self.view.textedit_infor.append(line)

    """
    area for thread exec get sub
    """

    def on_changed_value_table(self, row, col, value):
        print(row, col, value)
        self.model.update_row_col(row_index=row, col_index=col, new_data=value)
        print(self.model.get_all())

    def show_notify_loading(self):
        self.loading_dialog = LoadingDialog()
        self.loading_dialog.setWindowTitle("Đang xử lý hình ảnh...")
        self.loading_dialog.label.setText("Đang khởi tạo dữ liệu để xử lý...")
        self.loading_dialog.cancel_signal.connect(self.close_loading_dialog)
        self.loading_dialog.progress.setValue(1)
        self.loading_dialog.show()

    def show_final_value(self, value):
        if self.loading_dialog is None:
            return
        if self.thread_exec_get_sub is None:
            return
        try:
            for idx, v in enumerate(value):
                if "result_text" not in v or "frame_index" not in v:
                    continue
                table_rows = TableRow(
                    content=v["result_text"],
                    content_trans="",
                    current_time=v["frame_index"],
                )
                self.model.add_row(table_rows)
            self.add_data_to_table()
        except Exception as ex:
            print(ex)

    def close_loading_dialog(self):
        if self.loading_dialog is None:
            return
        if self.thread_exec_get_sub is None:
            return
        self.thread_exec_get_sub._running = False
        self.loading_dialog.close()

    def show_sum_progress(self, number):
        if number is None or number == "":
            return
        if self.loading_dialog is None:
            return
        self.loading_dialog.progress.setRange(0, number)

    def show_number_progress(self, number):
        if number is None or number == "":
            return
        if self.loading_dialog is None:
            return
        self.loading_dialog.progress.setValue(number)

    def show_mesage_progress(self, message):
        if message is None or message == "":
            return
        if self.loading_dialog is None:
            return
        self.loading_dialog.label.setText(message)

    def show_message_infor_progress(self, message):
        if message is None or message == "":
            return
        if self.loading_dialog is None:
            return
        self.loading_dialog.label_infor.setText(message)

    def finish_thread_get_sub(self):
        self.loading_dialog.close()
