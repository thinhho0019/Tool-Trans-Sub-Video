class OCRService:
    def __init__(self, lang="ch"):
        from paddleocr import PaddleOCR

        self.ocr = PaddleOCR(use_angle_cls=True, lang=lang)

    def perform_ocr(self, image_path):
        result = self.ocr.ocr(image_path)
        return result

    def extract_text(self, ocr_result):
        if isinstance(ocr_result, list) and len(ocr_result) > 0:
            return "".join([line[1][0] for line in ocr_result[0]])
        return ""
