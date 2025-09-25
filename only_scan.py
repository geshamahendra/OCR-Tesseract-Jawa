from PIL import Image, ImageFilter, ImageEnhance
import os
import pytesseract
import re

def preprocess_image(image):
    """Apply preprocessing to enhance OCR accuracy."""
    image = image.convert('L')  # Grayscale
    image = ImageEnhance.Contrast(image).enhance(1.05)
    image = image.filter(ImageFilter.GaussianBlur(radius=0.3))
    image = image.point(lambda p: 255 if p > 180 else 0)
    return image

def extract_text_from_images(
    images_folder,
    output_text_path,
    language,
    tessdata_prefix=None,
    tesseract_cmd=None,
    even_or_odd=None
):
    """Extract text from existing images using OCR."""
    if tessdata_prefix:
        os.environ['TESSDATA_PREFIX'] = tessdata_prefix
        print(f"Menggunakan direktori tessdata: {tessdata_prefix}")
    
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        print(f"Menggunakan executable Tesseract: {tesseract_cmd}")

    extracted_text = ""

    def extract_page_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else -1

    image_files = sorted(
        [f for f in os.listdir(images_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))],
        key=extract_page_number
    )
    
    if not image_files:
        print(f"Tidak ada gambar ditemukan di folder {images_folder}")
        return

    for image_file in image_files:
        page_num = int(''.join(filter(str.isdigit, image_file)))
        
        if even_or_odd == 'even' and page_num % 2 != 0:
            continue
        if even_or_odd == 'odd' and page_num % 2 == 0:
            continue

        image_path = os.path.join(images_folder, image_file)
        print(f"Memproses gambar {image_path}...")
        image = Image.open(image_path)
        preprocessed_image = preprocess_image(image)

        print(f"Melakukan OCR pada {image_file} dengan bahasa: {language}")
        text = pytesseract.image_to_string(preprocessed_image, lang=language)
        #extracted_text += f"\n--- Gambar {image_file} (halaman {page_num}) ---\n{text}\n"
        extracted_text += text

    try:
        with open(output_text_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        print(f"Teks hasil ekstraksi disimpan ke: {output_text_path}")
    except Exception as e:
        print(f"Gagal menyimpan teks: {e}")

    return extracted_text

if __name__ == "__main__":
    project_name = "ramayana"  # Nama project 
    ocr_language = "ramayana"  # Bahasa OCR (.traineddata)

    base_dir = f"scan_result/result_{project_name}"
    images_dir = os.path.join(base_dir, "images")
    output_text_file = os.path.join(base_dir, f"result_{project_name}.txt")

    tessdata_dir = "tesstrain/data"
    tesseract_path = "tesseract"  # Path executable Tesseract
    process_even_or_odd = None  # 'even', 'odd', None

    extract_text_from_images(
        images_folder=images_dir,
        output_text_path=output_text_file,
        language=ocr_language,
        tessdata_prefix=tessdata_dir,
        tesseract_cmd=tesseract_path,
        even_or_odd=process_even_or_odd
    )
