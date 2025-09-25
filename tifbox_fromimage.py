import os
import subprocess
from PIL import Image
import pytesseract

# Path ke executable Tesseract
# Sesuaikan dengan lokasi instalasi Tesseract di sistem Anda
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

def convert_to_tiff(image_path, tiff_path):
    """
    Konversi gambar input ke format TIFF.

    :param image_path: Path ke gambar input
    :param tiff_path: Path untuk menyimpan gambar dalam format TIFF
    """
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")  # Pastikan dalam format RGB
            img.save(tiff_path, format="TIFF")
        print(f"File .tif berhasil dihasilkan: {tiff_path}")
    except Exception as e:
        print(f"Error saat mengonversi ke TIFF: {e}")

def generate_tif_and_box(image_path, output_path):
    """
    Menggunakan Tesseract untuk menghasilkan file .tif dan .box dari gambar.

    :param image_path: Path ke gambar input
    :param output_path: Path lengkap untuk file output (termasuk direktori dan nama dasar tanpa ekstensi)
    """
    tiff_path = f"{output_path}.tif"

    # Konversi gambar ke TIFF
    convert_to_tiff(image_path, tiff_path)

    try:
        # Hasilkan file .box menggunakan Tesseract CLI
        subprocess.run([
            pytesseract.pytesseract.tesseract_cmd,
            tiff_path,  # Path ke file TIFF
            output_path,  # Path output lengkap dengan direktori dan nama dasar
            "-l", "eng",  # Bahasa Inggris
            "makebox"  # Mode untuk menghasilkan file .box
        ], check=True)

        print(f"File .box berhasil dihasilkan dengan nama dasar: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error saat menjalankan Tesseract: {e}")

# Contoh penggunaan
if __name__ == "__main__":
    # Path ke gambar input
    image_path = "pdf_to_txt/preprocessed_images/page_49.png"  # Ganti dengan path gambar Anda
    output_dir = "pdf_to_txt/preprocessed_images"  # Ganti dengan direktori output Anda
    output_basename = "ramayanav2"  # Nama dasar output (tanpa ekstensi)

    # Gabungkan direktori dan nama dasar untuk path output lengkap
    output_path = os.path.join(output_dir, output_basename)

    # Hasilkan file .tif dan .box
    generate_tif_and_box(image_path, output_path)

    # Pastikan file output berada di direktori yang sesuai
    tif_file = f"{output_path}.tif"
    box_file = f"{output_path}.box"

    if os.path.exists(tif_file) and os.path.exists(box_file):
        print(f"File .tif: {tif_file}")
        print(f"File .box: {box_file}")
    else:
        print("Gagal menghasilkan file output.")