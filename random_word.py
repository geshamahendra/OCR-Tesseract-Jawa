import random
import string

def generate_random_string_with_special_chars_and_spaces_per_line(line_count=5, length_per_line=100, space_prob=0.1):
    # Karakter yang dapat dipilih (huruf besar, huruf kecil, angka, dan huruf unik)
    characters = string.ascii_letters + string.digits + "ĀāĪīŪūÑñṄṅŊŋṢṣŚśṬṭḌḍÈèĔĕÉéÖöŎŏÔôÇç"
    result = []

    for _ in range(line_count):
        line = []
        for _ in range(length_per_line):
            # Dengan probabilitas tertentu, tambahkan spasi
            if random.random() < space_prob:
                line.append(' ')
            else:
                line.append(random.choice(characters))
        result.append(''.join(line))

    return '\n'.join(result)

def save_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# Menghasilkan beberapa baris dengan panjang tertentu
line_count = 500  # Jumlah baris
length_per_line = 100  # Panjang setiap baris
random_string = generate_random_string_with_special_chars_and_spaces_per_line(line_count, length_per_line)

# Menyimpan hasil ke dalam file
output_filename = 'langdata/lat_java.sample_text'  # Nama file output
save_to_file(output_filename, random_string)

print(f"Hasil disimpan dalam file: {output_filename}")
