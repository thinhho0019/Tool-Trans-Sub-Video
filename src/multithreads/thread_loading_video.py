import time

import cv2
from PyQt6.QtCore import QMutex, QThread, QWaitCondition, pyqtSignal, pyqtSlot


class ThreadLoadingVideo(QThread):
    frame_signal = pyqtSignal(object)
    finished = pyqtSignal()
    range_video = pyqtSignal(int)
    current_duration = pyqtSignal(int)
    data_infor = pyqtSignal(dict)

    def __init__(self, path_video):
        super().__init__()
        self.path_video = path_video
        self._running = True
        self._paused = False
        self._seek_frame = None
        self._fps_video = None
        self._mutex = QMutex()
        self._pause_cond = QWaitCondition()

    def run(self):
        cap = cv2.VideoCapture(self.path_video)
        self._fps_video = cap.get(cv2.CAP_PROP_FPS)
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        resolution = f"{width}x{height}"
        duration_seconds = total_frames / self._fps_video if self._fps_video > 0 else 0
        self.range_video.emit(int(duration_seconds))
        self.data_infor.emit(
            {
                "fps": self._fps_video,
                "resolution": resolution,
                "duration": str(duration_seconds),
                "qrect": "",
                "direct_video": self.path_video,
            }
        )
        while self._running:
            self._mutex.lock()
            if self._paused:
                self._pause_cond.wait(self._mutex)
            self._mutex.unlock()

            if self._seek_frame is not None:
                cap.set(cv2.CAP_PROP_POS_FRAMES, self._seek_frame)
                self._seek_frame = None

            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
            current_seconds = (
                int(current_frame / self._fps_video) if self._fps_video > 0 else 0
            )
            self.current_duration.emit(current_seconds)
            self.frame_signal.emit(frame)
            time.sleep(1 / self._fps_video if self._fps_video > 0 else 0.03)

        cap.release()
        self.finished.emit()

    @pyqtSlot()
    def stop_video(self):
        self._running = False
        self._pause_cond.wakeAll()  # nếu đang pause thì wake luôn để thoát

    @pyqtSlot()
    def pause_video(self):
        self._paused = True

    @pyqtSlot()
    def continue_video(self):
        self._mutex.lock()
        self._paused = False
        self._pause_cond.wakeAll()
        self._mutex.unlock()

    @pyqtSlot(int)
    def seek(self, frame_number):
        if self._fps_video is None:
            return
        self._mutex.lock()
        self._seek_frame = frame_number * self._fps_video
        if self._paused:
            self._pause_cond.wakeAll()
        self._mutex.unlock()
