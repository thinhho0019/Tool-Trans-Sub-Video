import threading
from queue import Queue

from src.services.ocr_service import OCRService


class OcrPool:
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, pool_size=8, lang="ch"):
        if getattr(self, "_initialized", False):
            return  # Đã init rồi thì bỏ qua

        self.pool_size = pool_size
        self.lang = lang
        self.pool = Queue()
        self.thread_init = None
        self._lock = threading.Lock()

        self._initialized = True  # 🔥 Đánh dấu đã init rồi

    @property
    def is_initializing(self):
        return self.thread_init is not None and self.thread_init.is_alive()

    def init_pool(self):
        with self._lock:
            if self.is_initializing:
                print("[POOL] Đang khởi tạo, vui lòng chờ...")
                return False

            def thread_init_pool():
                try:
                    for index in range(self.pool_size):
                        print(f"[INIT] Đang khởi tạo OCR luồng {index + 1}")
                        self.pool.put(OCRService(lang=self.lang))
                except Exception as e:
                    print("[ERROR] Lỗi khi init pool:", e)
                finally:
                    with self._lock:
                        self.thread_init = None
                        print("[DEBUG] Reset thread_init")

            self.thread_init = threading.Thread(target=thread_init_pool, daemon=True)
            self.thread_init.start()
            return

    def acquire(self):
        return self.pool.get()

    def release(self, ocr_instance):
        self.pool.put(ocr_instance)
