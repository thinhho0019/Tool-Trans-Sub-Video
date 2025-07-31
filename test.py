from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # 'ch' = Chinese (Simplified)
result = ocr.ocr(
    r"C:\Users\ADMIN\Desktop\tool-video-sub\Screenshot 2025-07-31 110200.png"
)

"""
array to string obj
"""
string_obj = "".join(result[0]["rec_texts"])


print(string_obj)
