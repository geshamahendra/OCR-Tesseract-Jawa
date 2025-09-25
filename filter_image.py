from pdf2image import convert_from_path
from PIL import ImageFilter, ImageEnhance
import os

def preprocess_images_from_pdf(file_path, page_ranges, output_image_folder):
    """
    Extracts and preprocesses images from a PDF file.
    
    Parameters:
    - file_path: str, path to the PDF file.
    - page_ranges: list of tuples, where each tuple specifies a range of pages (start, end).
    - output_image_folder: str, folder path to save the preprocessed images.
    
    Returns:
    - None, saves the preprocessed images to the specified folder.
    """
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
                blurred_image = image.filter(ImageFilter.GaussianBlur(radius=1))  # Reduce noise
                enhancer = ImageEnhance.Contrast(blurred_image)  # Enhance contrast
                enhanced_image = enhancer.enhance(1.2)  # Increase contrast (value > 1)
                threshold_image = enhanced_image.point(lambda p: p > 200 and 255)  # Apply threshold
                
                # Save preprocessed image
                image_name = f"page_{page_number + 1}.png"
                image_path = os.path.join(output_image_folder, image_name)
                threshold_image.save(image_path)
                print(f"Preprocessed image saved at {image_path}")
    
    except Exception as e:
        print(f"Error processing PDF: {e}")

if __name__ == "__main__":
    # Define the input PDF and output image folder paths
    pdf_file_path = "scan_source/KBG_281_001.pdf"  # Replace with your PDF file path
    output_image_folder = "preprocessed_images/siyem"  # Replace with your chosen folder
    os.makedirs(output_image_folder, exist_ok=True)  # Create folder if it doesn't exist

    # Specify the page ranges to process as tuples (start_page, end_page)
    page_ranges = [(3, 23)]  # Adjust page ranges as needed

    # Preprocess and save images from the specified PDF pages
    preprocess_images_from_pdf(pdf_file_path, page_ranges, output_image_folder)
