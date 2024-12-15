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

def generate_training_data(image_path, output_path, lang_code="eng"):
    """
    Menjalankan langkah-langkah pelatihan Tesseract untuk menghasilkan file pelatihan tambahan.
    :param image_path: Path ke gambar input
    :param output_path: Path lengkap untuk file output
    :param lang_code: Kode bahasa untuk pelatihan (default: "eng")
    """
    # Langkah pertama: Menghasilkan .tif dan .box
    generate_tif_and_box(image_path, output_path)

    # Langkah kedua: Menghasilkan file .tr (training data)
    try:
        subprocess.run([
            pytesseract.pytesseract.tesseract_cmd,
            f"{output_path}.tif",  # File TIFF
            f"{output_path}.tr",  # Output file training
            "-l", lang_code,  # Kode bahasa
            "train"  # Mode pelatihan
        ], check=True)
        print(f"File training .tr berhasil dihasilkan: {output_path}.tr")
    except subprocess.CalledProcessError as e:
        print(f"Error saat menghasilkan training data: {e}")

    # Langkah ketiga: Menghasilkan file unicharset
    try:
        subprocess.run([
            pytesseract.pytesseract.tesseract_cmd,
            f"{output_path}.tif",  # File TIFF
            f"{output_path}.unicharset",  # Output unicharset
            "-l", lang_code,  # Kode bahasa
            "unicharset"  # Mode untuk menghasilkan unicharset
        ], check=True)
        print(f"File unicharset berhasil dihasilkan: {output_path}.unicharset")
    except subprocess.CalledProcessError as e:
        print(f"Error saat menghasilkan unicharset: {e}")

    # Langkah keempat: Menghasilkan file inttemp, normproto, shapetable, pffmtable
    try:
        subprocess.run([
            pytesseract.pytesseract.tesseract_cmd,
            f"{output_path}.tif",  # File TIFF
            f"{output_path}.traineddata",  # Output traineddata
            "-l", lang_code,  # Kode bahasa
            "train"  # Proses pelatihan untuk menghasilkan file tambahan
        ], check=True)
        print(f"File pelatihan lengkap berhasil dihasilkan: {output_path}.traineddata")
    except subprocess.CalledProcessError as e:
        print(f"Error saat menghasilkan trained data: {e}")

# Contoh penggunaan
if __name__ == "__main__":
    # Path ke gambar input
    image_path = "pdf_to_txt/preprocessed_images/page_49.png"  # Ganti dengan path gambar Anda
    output_dir = "pdf_to_txt/preprocessed_images"  # Ganti dengan direktori output Anda
    output_basename = "ramayanav2"  # Nama dasar output (tanpa ekstensi)

    # Gabungkan direktori dan nama dasar untuk path output lengkap
    output_path = os.path.join(output_dir, output_basename)

    # Hasilkan data pelatihan
    generate_training_data(image_path, output_path)

    # Pastikan file output berada di direktori yang sesuai
    required_files = [
        f"{output_path}.tif",
        f"{output_path}.box",
        f"{output_path}.unicharset",
        f"{output_path}.traineddata",
        f"{output_path}.inttemp",
        f"{output_path}.normproto",
        f"{output_path}.shapetable",
        f"{output_path}.pffmtable"
    ]

    for file in required_files:
        if os.path.exists(file):
            print(f"File berhasil dihasilkan: {file}")
        else:
            print(f"Gagal menghasilkan file: {file}")
