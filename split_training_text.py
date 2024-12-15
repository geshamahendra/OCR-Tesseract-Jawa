import os
import random
import pathlib
import subprocess

# File teks input
training_text_file = 'langdata/lat_java.training' #diganti

# Direktori output
output_directory = 'tesstrain/data/lat_java-ground-truth' #diganti
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Baca dan acak baris dari file input
with open(training_text_file, 'r') as input_file:
    lines = [line.strip() for line in input_file if line.strip()]

random.shuffle(lines)

# Batasi jumlah baris yang akan diproses
count = 1000
lines = lines[:count]

# Proses setiap baris
for line_count, line in enumerate(lines):
    # Nama file dasar untuk output
    training_text_file_name = pathlib.Path(training_text_file).stem
    line_training_text = os.path.join(output_directory, f'{training_text_file_name}_{line_count}.gt.txt')
    file_base_name = f'lat_java_{line_count}' #diganti
    output_image_base = os.path.join(output_directory, file_base_name)

    # Tulis baris ke file .gt.txt
    with open(line_training_text, 'w') as output_file:
        output_file.write(line)

    # Jalankan perintah text2image
    result = subprocess.run([
        'text2image',
        '--font=Times New Roman',
        f'--text={line_training_text}',
        f'--outputbase={output_image_base}',
        '--max_pages=1',
        '--strip_unrenderable_words',
        '--leading=32',
        '--xsize=3600',
        '--ysize=480',
        '--char_spacing=1',
        '--exposure=0',
        '--unicharset_file=/Users/geshamahendra/My_Home/ocr_tesseract/create_box_unichar/output.unicharset' #diganti
    ], capture_output=True, text=True)

    # Periksa jika terjadi kesalahan
    if result.returncode != 0:
        print(f"Error processing line {line_count}: {line}")
        print(f"Error message: {result.stderr}")
        # Hapus file yang tidak lengkap
        if os.path.exists(line_training_text):
            os.remove(line_training_text)
        if os.path.exists(f"{output_image_base}.tif"):
            os.remove(f"{output_image_base}.tif")
        continue

    print(f"Successfully created: {line_training_text} and {output_image_base}.tif")

print("Processing complete.")