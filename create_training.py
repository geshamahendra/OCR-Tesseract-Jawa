import os
import subprocess

# Tentukan path ke folder tesstrain
tesstrain_path = "/path/to/tesstrain"
image_path = os.path.join(tesstrain_path, "images")

# Tentukan bahasa dan output traineddata
lang = "your_language_code"  # Contoh: "eng"
output_dir = os.path.join(tesstrain_path, "traineddata")

# Proses training menggunakan Tesseract
def train_tesseract():
    # Pastikan folder output ada
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Tentukan perintah untuk melatih
    command = [
        "tesseract",
        image_path,  # Folder yang berisi gambar dan file .box
        os.path.join(output_dir, lang),  # Hasil output
        "--psm", "6",  # Tentukan mode halaman (optional)
        "batch.nochop",  # Parameter untuk batch processing
        "makebox",  # Buat file .box jika belum ada
        "train",  # Gunakan mode pelatihan
    ]
    
    # Jalankan perintah Tesseract untuk pelatihan
    subprocess.run(command)

if __name__ == "__main__":
    train_tesseract()
