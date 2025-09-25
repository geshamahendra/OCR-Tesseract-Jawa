import os
import pathlib
import subprocess

# File teks input
training_text_file = 'langdata/Jawa.training_text'  # Ganti sesuai kebutuhan

# Direktori output
output_directory = 'tesstrain/data/Jawa-ground-truth'  # Ganti sesuai kebutuhan
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Hapus file lama (.tif, .box, .gt.txt, dan .lstmf)
print("Menghapus file lama...")
for file_ext in ['.tif', '.box', '.gt.txt', '.lstmf']:
    for file in pathlib.Path(output_directory).glob(f"*{file_ext}"):
        file.unlink()
print("File lama berhasil dihapus.")

# Baca baris dari file teks input
print("Membaca file teks input...")
with open(training_text_file, 'r') as input_file:
    lines = [line.strip() for line in input_file if line.strip()]

# Batasi jumlah baris yang akan diproses (jika diperlukan)
count = 40000  # Ganti sesuai kebutuhan
lines = lines[:count]  # Ambil maksimal `count` baris dari file input

# Proses setiap baris
print("Memulai proses pembuatan dataset...")
for line_count, line in enumerate(lines):
    # Nama file dasar untuk output
    training_text_file_name = pathlib.Path(training_text_file).stem
    line_training_text = os.path.join(output_directory, f'{training_text_file_name}_{line_count}.gt.txt')
    file_base_name = f'Jawa_{line_count}'
    output_image_base = os.path.join(output_directory, file_base_name)

    try:
        # 1. Buat file .gt.txt
        with open(line_training_text, 'w') as output_file:
            output_file.write(line)

        # 2. Jalankan perintah text2image
        result = subprocess.run([
            'text2image',
            '--font=ramayana',  # Ganti sesuai dengan font aksara Jawa Anda
            f'--text={line_training_text}',
            f'--outputbase={output_image_base}',
            '--max_pages=1',
            '--strip_unrenderable_words',
            '--leading=32',
            '--xsize=3600',
            '--ysize=480',
            '--char_spacing=1',
            '--exposure=0',
            '--unicharset_file=langdata/Jawa.unicharset'  # Ganti jika diperlukan
        ], capture_output=True, text=True)

        # 3. Periksa apakah perintah berhasil
        if result.returncode != 0:
            raise RuntimeError(f"Error generating image: {result.stderr}")

        # 4. Validasi file .tif yang dihasilkan
        tif_file = f"{output_image_base}.tif"
        if not os.path.exists(tif_file):
            raise FileNotFoundError(f"File .tif tidak ditemukan: {tif_file}")

        # 5. Validasi file .box
        box_file = f"{output_image_base}.box"
        if not os.path.exists(box_file):
            raise FileNotFoundError(f"File .box tidak ditemukan: {box_file}")

        print(f"Successfully created: {line_training_text}, {tif_file}, and {box_file}")

    except Exception as e:
        print(f"Error processing line {line_count}: {line}")
        print(f"Error message: {e}")
        # Hapus file yang tidak lengkap
        for file in [line_training_text, f"{output_image_base}.tif", f"{output_image_base}.box"]:
            if os.path.exists(file):
                os.remove(file)
        continue

print("Proses pembuatan dataset selesai.")
