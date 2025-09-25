# Daftar aksara Jawa dasar
aksara_jawa = [
    'ꦏ', 'ꦑ', 'ꦒ', 'ꦓ', 'ꦔ', 'ꦲ', 'ꦲ',
    'ꦕ', 'ꦖ', 'ꦗ', 'ꦚ', 'ꦯ',
    'ꦪ', 'ꦛ', 'ꦜ', 'ꦝ', 'ꦞ', 'ꦟ',
    'ꦰ', 'ꦫ', 'ꦠ', 'ꦡ', 'ꦢ', 'ꦣ',
    'ꦤ', 'ꦱ', 'ꦭ', 'ꦥ', 'ꦦ', 'ꦧ',
    'ꦨ', 'ꦩ', 'ꦮ'
]

# Daftar sandhangan
sandhangan = [
    '', 'ꦴ', 'ꦶ', 'ꦷ', 'ꦸ', 'ꦹ', 'ꦼ', 'ꦺ', 'ꦺꦴ', 'ꦻꦴ', 'ꦀ', 'ꦁ', 'ꦂ', 'ꦃ',
    'ꦼꦴ','꧀'
]

simbol = [
    'ꧏ', '꧊', '꧋', '꧌', '꧍', '꧁', '꧂', '꧃', '꧄', '꧅',
    '꧉', '꧈', '꧇'
]

swara = [
'ꦉ', 'ꦊ', 'ꦉꦴ', 'ꦋ', 'ꦄ', 'ꦅ', 'ꦈ', 'ꦌ', 'ꦎ'
'ꦇ', 'ꦈꦴ', 'ꦎꦴ', 'ꦍ'
]

angka = [
     '꧒', '꧓', '꧔', '꧕', '꧖', '꧘', '꧐', 'ꦘ', 'ꦐ', 'ꦙ'
]
# Daftar aksara yang bisa ditumpuk
aksara_tumpuk = [
    '꧀ꦏ', '꧀ꦑ', '꧀ꦒ', '꧀ꦓ', '꧀ꦔ', '꧀ꦲ', '꧀ꦲ', 
    '꧀ꦕ', '꧀ꦖ', '꧀ꦗ', '꧀ꦙ', '꧀ꦚ', '꧀ꦯ',
    '꧀ꦪ', '꧀ꦛ', '꧀ꦜ', '꧀ꦝ', '꧀ꦞ', '꧀ꦟ',
    '꧀ꦰ', '꧀ꦫ', '꧀ꦠ', '꧀ꦡ', '꧀ꦢ', '꧀ꦣ',
    '꧀ꦤ', '꧀ꦱ', '꧀ꦭ', '꧀ꦥ', '꧀ꦦ', '꧀ꦧ',
    '꧀ꦨ', '꧀ꦩ'
]

aksara_khusus = [
    'ꦾ', 'ꦿ', '꧀ꦮ'
]

aksara_spesial = [
     'ꦽ', '꧀ꦭꦼ', 'ꦽꦴ', '꧀ꦭꦼꦴ'
]
# Fungsi untuk memecah kombinasi menjadi baris-baris tanpa memutus ligatur
def split_into_lines_no_cut(combinations, max_length=100):
    lines = []
    current_line = ""

    for combination in combinations:
        # Jika menambahkan kombinasi ini melebihi batas panjang, pindahkan ke baris baru
        if len(current_line) + len(combination) > max_length:
            if current_line:
                lines.append(current_line)
            current_line = combination  # Mulai baris baru dengan kombinasi ini
        else:
            current_line += combination  # Tambahkan kombinasi ke baris saat ini

    # Jangan lupa untuk menambahkan baris terakhir
    if current_line:
        lines.append(current_line)

    return lines

# Fungsi untuk menghasilkan kombinasi berdasarkan kategori tanpa memutus ligatur
def generate_combinations_with_safe_split(aksara, sandhangan, aksara_tumpuk, aksara_khusus, simbol, swara, angka, max_length=100):
    results = {
        "tanpa_sandhangan": [],
        "dengan_sandhangan": [],
        "tumpuk": [],
        "tumpuk_dengan_sandhangan": [],
        "tumpuk_khusus": [],
        "tumpuk_khusus_dengan_sandhangan": [],
        "dengan_swara": [],
        "dengan_simbol": [],
        "dengan_angka": [],
        "dengan_spesial": []
    }

    for a in aksara:
        # Kombinasi aksara tanpa sandhangan
        results["tanpa_sandhangan"].append(a)

        # Kombinasi aksara dengan sandhangan
        results["dengan_sandhangan"].extend([a + s for s in sandhangan])

        # Kombinasi aksara dengan tumpukan
        results["tumpuk"].extend([a + t for t in aksara_tumpuk])

        # Kombinasi aksara dengan tumpukan dan sandhangan
        results["tumpuk_dengan_sandhangan"].extend([a + t + s for t in aksara_tumpuk for s in sandhangan])

        # Kombinasi aksara dengan tumpukan khusus
        results["tumpuk_khusus"].extend([a + k for k in aksara_khusus])

        # Kombinasi aksara dengan tumpukan khusus dan sandhangan
        results["tumpuk_khusus_dengan_sandhangan"].extend([a + k + s for k in aksara_khusus for s in sandhangan])

        # Kombinasi aksara dengan swara
        results["dengan_swara"].extend([a + S for S in swara])

        # Kombinasi aksara dengan simbol
        results["dengan_simbol"].extend([a + M for M in simbol])
        
        # Kombinasi aksara dengan angka
        results["dengan_angka"].extend([a + A for A in angka])

        # Kombinasi spesial
        results["dengan_spesial"].extend([a + x for x in aksara_spesial])

    # Gabungkan semua aksara tanpa sandhangan dalam satu baris
    results["tanpa_sandhangan"] = [''.join(results["tanpa_sandhangan"])]

    # Pecah setiap kategori menjadi baris-baris tanpa memutus ligatur
    for category in results:
        results[category] = split_into_lines_no_cut(results[category], max_length)

    return results

# Hasilkan semua kombinasi
combinations_safe_split = generate_combinations_with_safe_split(
    aksara_jawa, sandhangan, aksara_tumpuk, aksara_khusus, simbol, swara, angka, max_length=100
)

# Simpan hasil ke satu file dengan pembatasan panjang baris tanpa memutus ligatur
with open('sample_text_jawa/kombinasi_aksara_jawa_safe_split.txt', 'w', encoding='utf-8') as file:
    for category, combinations in combinations_safe_split.items():
        file.write('\n'.join(combinations) + '\n')

print("Kombinasi aksara Jawa dengan batas panjang baris tanpa memutus ligatur telah disimpan.")
