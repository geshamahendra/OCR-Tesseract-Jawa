import pytesseract
from PIL import Image

# Tentukan path ke traineddata
traineddata_path = "tesstrain/data/eng_jawa.traineddata"

# Gambar yang akan diuji
img = Image.open("preprocessed_images/page_49.png")

# Menggunakan Tesseract OCR dengan traineddata baru
custom_oem_psm_config = r'--oem 3 --psm 6 -l eng_jawa'
text = pytesseract.image_to_string(img, config=custom_oem_psm_config)

print(text)
