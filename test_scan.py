import os
from pdf2image import convert_from_path
import pytesseract
from PIL import ImageFilter, ImageEnhance

def ensure_folder_exists(folder_path):
    """Create folder if it doesn't exist."""
    os.makedirs(folder_path, exist_ok=True)

def preprocess_image(image):
    """Apply preprocessing to enhance OCR accuracy."""
    image = image.convert('L')  # Convert to grayscale
    image = ImageEnhance.Contrast(image).enhance(1.05)
    image = image.filter(ImageFilter.GaussianBlur(radius=0.3))
    image = image.point(lambda p: 255 if p > 180 else 0)
    return image

def extract_text_from_pdf(
    pdf_path,
    output_folder,
    output_text_path,
    page_ranges=[(1, 1)],
    language=None,
    tessdata_prefix=None,
    tesseract_cmd=None,
    even_or_odd=None
):
    """Extract text from PDF using OCR with optional preprocessing."""
    if language is None:
        raise ValueError("Parameter 'language' harus ditentukan! Tidak ada nilai default.")
    
    if tessdata_prefix:
        os.environ['TESSDATA_PREFIX'] = tessdata_prefix
        print(f"Menggunakan direktori tessdata: {tessdata_prefix}")
    
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        print(f"Menggunakan executable Tesseract: {tesseract_cmd}")
    
    # Cek apakah traineddata untuk bahasa yang dipilih tersedia
    if tessdata_prefix:
        traineddata_path = os.path.join(tessdata_prefix, f"{language}.traineddata")
        if os.path.exists(traineddata_path):
            print(f"Model bahasa '{language}' ditemukan dan akan digunakan.")
        else:
            print(f"PERINGATAN: Model bahasa '{language}' tidak ditemukan di {tessdata_prefix}")
            print("Pastikan file traineddata yang benar sudah diinstal atau tentukan TESSDATA_PREFIX yang benar.")

    ensure_folder_exists(output_folder)
    ensure_folder_exists(os.path.dirname(output_text_path))
    
    extracted_text = ""
    
    try:
        print("Mengkonversi PDF ke gambar...")
        images = convert_from_path(pdf_path, 300)
        total_pages = len(images)
        print(f"Total halaman: {total_pages}")
        
        for start, end in page_ranges:
            for page_index in range(start - 1, min(end, total_pages)):
                page_num = page_index + 1
                
                if even_or_odd == 'even' and page_num % 2 != 0:
                    continue
                if even_or_odd == 'odd' and page_num % 2 == 0:
                    continue
                
                print(f"Memproses halaman {page_num}...")
                preprocessed_image = preprocess_image(images[page_index])
                image_name = f"page_{page_num}.png"
                image_path = os.path.join(output_folder, image_name)
                preprocessed_image.save(image_path)
                print(f"Menyimpan gambar yang telah diproses: {image_path}")
                
                print(f"Melakukan OCR dengan bahasa: {language}")
                text = pytesseract.image_to_string(preprocessed_image, lang=language)
                #extracted_text += f"\n--- Halaman {page_num} ---\n{text}\n"
                extracted_text += text
                
    except Exception as e:
        print(f"Error saat mengkonversi atau memproses gambar: {e}")
    
    try:
        with open(output_text_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)
        print(f"Teks hasil ekstraksi disimpan ke: {output_text_path}")
    except Exception as e:
        print(f"Gagal menyimpan teks: {e}")
    
    return extracted_text

if __name__ == "__main__":
    # === CONFIGURASI YANG MUDAH DIUBAH ===
    project_name = "smaradahana"    # Nama folder hasil
    ocr_language = "kakawin"  # Bahasa OCR, BISA DIGANTI-BEBAS

    pdf_file = f"scan_source/Smaradahana_250517_152748.pdf"
    output_image_dir = f"scan_result/result_{project_name}/images"
    output_text_file = f"scan_result/result_{project_name}/result_{project_name}.txt"
    pages_to_process = [(13, 126)]  # Bisa banyak range [(1,5), (10,12), dst.]

    tessdata_dir = "tesstrain/data"
    tesseract_path = "tesseract"
    process_even_or_odd = None  # 'even', 'odd', atau None

    extract_text_from_pdf(
        pdf_path=pdf_file,
        output_folder=output_image_dir,
        output_text_path=output_text_file,
        page_ranges=pages_to_process,
        language=ocr_language,
        tessdata_prefix=tessdata_dir,
        tesseract_cmd=tesseract_path,
        even_or_odd=process_even_or_odd
    )
