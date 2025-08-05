import time
from concurrent.futures import ThreadPoolExecutor

import cv2
import natsort
from PyQt6.QtCore import QThread, pyqtSignal


class ThreadGetSubVideo(QThread):
    show_control = pyqtSignal()
    sum_progress = pyqtSignal(int)
    number_progress = pyqtSignal(int)
    message_progress = pyqtSignal(str)
    message_infor_progress = pyqtSignal(str)
    final_value = pyqtSignal(list)

    def __init__(self, path_video, qrect, pool, interval_sec=1):
        super().__init__()
        self.path_video = path_video
        self._running = True
        self._qrect = qrect
        self._pool = pool
        self.interval_sec = interval_sec
        self._result_ocr = []

    def run(self):
        self.exc_get_frame()

    def exc_get_frame(self):
        self.show_control.emit()
        cap = cv2.VideoCapture(self.path_video)
        total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        self.sum_progress.emit(int(total_frames))

        frame_index = 0
        next_frame = 0
        # init thread queue for ocr
        while self._pool.is_initializing:
            self.message_progress.emit(
                f"Đang load model OCR({self._pool.pool_size} luồng)"
            )
            time.sleep(1)
            continue
        self.message_progress.emit(f"Đã load model OCR({self._pool.pool_size} luồng)")
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = []
            while self._running:
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_index >= next_frame:
                    self.number_progress.emit(frame_index)
                    # Submit xử lý frame
                    future = executor.submit(
                        self.exec_image_rect, frame.copy(), frame_index, self._pool
                    )
                    futures.append(future)
                    next_frame += int(self.interval_sec * fps)

                frame_index += 1

            # Đợi và xử lý kết quả
            for future in futures:
                try:
                    result_text = future.result()
                    self.message_progress.emit(result_text)
                except Exception as e:
                    print(f"Thread error: {e}")

        cap.release()
        # sort _result ocr
        self._result_ocr = natsort.natsorted(
            self._result_ocr, key=lambda x: x["frame_index"]
        )
        self.final_value.emit(self._result_ocr)
        self.finished.emit()

    def exec_image_rect(self, image, idx, pool):
        ocr = pool.acquire()
        try:
            if image is None:
                return f"Frame {idx}: Empty"
            x = int(self._qrect.x())
            y = int(self._qrect.y())
            w = int(self._qrect.width())
            h = int(self._qrect.height())
            cropped = image[y : y + h, x : x + w]

            # Encode to bytes
            _, buffer = cv2.imencode(".jpg", cropped)
            image_bytes = buffer.tobytes()

            # ⚠️ Tạo OCR riêng mỗi thread

            text = ocr.perform_ocr(image_bytes)
            print(text)
            self.message_infor_progress.emit(f"Đã lấy text thành công - {text}")
            self._result_ocr.append({"frame_index": idx, "result_text": text})
            return f"Frame {idx}: {text}"

        except Exception as e:
            return f"Frame {idx}: Error - {e}"
        finally:
            pool.release(ocr)

    def show_message_init_ocr(self, message):
        print(message)
        if message is None or message == "":
            return
        self.message_progress.emit(message)
