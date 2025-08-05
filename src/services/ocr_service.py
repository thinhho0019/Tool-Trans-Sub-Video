import cv2
import numpy as np


class OCRService:
    def __init__(self, lang="ch"):
        from paddleocr import PaddleOCR

        self.ocr = PaddleOCR(use_angle_cls=True, lang=lang)

    def perform_ocr(self, image_byte):
        nparr = np.frombuffer(image_byte, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        result = self.ocr.predict(image)
        return self.extract_text(result)

    def extract_text(self, ocr_result):
        try:
            string_obj = "".join(ocr_result[0]["rec_texts"])
            return string_obj
        except Exception:
            return ""
