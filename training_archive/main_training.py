from PIL import Image, ImageDraw, ImageFont
import os

# Direktori output untuk menyimpan gambar dan transkrip
output_dir = "pdf_to_txt/training/training_data"
os.makedirs(output_dir, exist_ok=True)

# Konfigurasi font dan ukuran
font_path = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"  # Ganti dengan font diakritik yang sesuai
font_size = 32
font = ImageFont.truetype(font_path, font_size)

# Contoh teks untuk pelatihan
training_text = [
    "Hana sira ratu dibya rĕṅön",
    "praśāsta riṅ rāt musuh nira praṇata",
    "jaya paṇḍita riṅ aji kabèh",
    "saṅ Daśaratha nāma tamoli",
    "bhaṭāra wiṣṇu Rāgādi musuh "


]

# Buat gambar untuk setiap baris teks
for idx, line in enumerate(training_text):
    image_width = 800
    image_height = 100
    image = Image.new("L", (image_width, image_height), color=255)  # Gambar hitam-putih
    draw = ImageDraw.Draw(image)
    
    # Tulis teks ke dalam gambar
    text_position = (10, 10)
    draw.text(text_position, line, font=font, fill=0)

    # Simpan gambar dan transkripsi
    image.save(f"{output_dir}/line_{idx + 1}.tif")
    with open(f"{output_dir}/line_{idx + 1}.gt.txt", "w", encoding="utf-8") as f:
        f.write(line)

print(f"Data pelatihan disimpan di: {output_dir}")
