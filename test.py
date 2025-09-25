import os
import pytesseract
from PIL import Image

# Pastikan TESSDATA_PREFIX benar
os.environ['TESSDATA_PREFIX'] = '/Users/geshamahendra/My_Home/ocr_tesseract/tesstrain/data'
pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'  # atau sesuaikan kalau path tesseract kamu beda

# Coba OCR sederhana
image_path = 'scan_result/result_adiparwa/page_8.png'  # Gambar kamu
image = Image.open(image_path)
text = pytesseract.image_to_string(image, lang='lat_jawa')

print(text)
