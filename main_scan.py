from pdf2image import convert_from_path
import pytesseract
from PIL import ImageFilter, ImageEnhance
import os

# Menetapkan path ke file Tesseract jika tidak ada dalam PATH
#pytesseract.pytesseract.tesseract_cmd = r"tesseract"  # Ganti dengan path tesseract Anda jika berbeda

# Menetapkan path ke folder tessdata jika menggunakan trained data khusus
#tesseract_data_path = "/usr/local/share/tessdata/eng_jawa.traineddata"  # Ganti dengan path tessdata Anda
#os.environ['TESSDATA_PREFIX'] = tesseract_data_path  # Tentukan direktori tessdata

def extract_text_from_image_pdf(file_path, page_ranges, output_image_folder):
    """
    Extracts text from a PDF file that contains images using OCR with preprocessing.
    
    Parameters:
    - file_path: str, path to the PDF file.
    - page_ranges: list of tuples, where each tuple specifies a range of pages (start, end).
    - output_image_folder: str, folder path to save the preprocessed images.
    
    Returns:
    - str, extracted text.
    """
    extracted_text = ""
    
    try:
        # Convert PDF pages to images
        print("Converting PDF pages to images...")
        images = convert_from_path(file_path, 300)  # 300 DPI for better quality
        total_pages = len(images)
        
        for start, end in page_ranges:
            # Ensure the page range is valid
            if start < 1 or end > total_pages or start > end:
                print(f"Invalid page range: {start}-{end}. Skipping.")
                continue
            
            for page_number in range(start - 1, end):
                print(f"Processing page {page_number + 1}...")
                
                # Preprocessing: Convert to grayscale, enhance contrast, and apply threshold
                image = images[page_number].convert('L')  # Convert to grayscale
                # Apply Gaussian Blur to reduce noise
                blurred_image = image.filter(ImageFilter.GaussianBlur(radius=1))  # Radius menentukan kekuatan blur
                enhancer = ImageEnhance.Contrast(image)  # Enhance contrast
                enhanced_image = enhancer.enhance(1.2)  # Increase contrast (value > 1)
                threshold_image = enhanced_image.point(lambda p: p > 200 and 255)  # Apply threshold (binary image)
                
                # Save preprocessed image for tuning
                image_name = f"page_{page_number + 1}.png"
                image_path = os.path.join(output_image_folder, image_name)
                threshold_image.save(image_path)
                print(f"Preprocessed image saved at {image_path}")
                
                # Perform OCR on the preprocessed image
                text = pytesseract.image_to_string(threshold_image, lang='lat_java')
                extracted_text += text + "\n"
    
    except Exception as e:
        print(f"Error processing PDF: {e}")
    
    return extracted_text


def save_text_to_file(output_path, text):
    """Save the extracted text to a file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(text)
        print(f"Text saved to {output_path}")
    except Exception as e:
        print(f"Error saving text to file: {e}")


if __name__ == "__main__":
    # Define the input PDF and output text file paths
    pdf_file_path = "scan_source/kakawin hariwaṅśa mpu panuluḥ .pdf"  # Ganti dengan path file PDF Anda
    output_txt_path = "scan_result/result_hariwangsa.txt"  # Ganti dengan path file output TXT Anda

    # Specify the folder where preprocessed images will be saved
    output_image_folder = "scan_result/result_hariwangsa"  # Ganti dengan folder yang Anda pilih
    os.makedirs(output_image_folder, exist_ok=True)  # Buat folder jika belum ada

    # Specify the page ranges to process as tuples (start_page, end_page)
    # For example: [(1, 10), (5, 6)] 82
    page_ranges = [(12, 12)]  # Ubah rentang halaman sesuai kebutuhan Anda

    # Extract text from the specified PDF pages
    extracted_text = extract_text_from_image_pdf(pdf_file_path, page_ranges, output_image_folder)

    # Save the extracted text to the output file
    if extracted_text:
        save_text_to_file(output_txt_path, extracted_text)
    else:
        print("No text extracted or invalid page ranges.")
