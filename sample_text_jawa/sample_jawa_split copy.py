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
# Fungsi untuk memecah kombinasi menjadi baris-baris yang tidak melebihi 20 karakter
def split_into_lines(text, max_length=100):
    lines = []
    current_line = ""
    
    # Pecah berdasarkan spasi tanpa memisahkan ligatur
    for part in text.split(" "):
        # Jika penambahan part ini melebihi max_length, buat baris baru
        if len(current_line + part) > max_length:
            lines.append(current_line)
            current_line = part  # Mulai baris baru dengan part ini
        else:
            # Tambahkan part ke baris saat ini
            if current_line:
                current_line += " " + part
            else:
                current_line = part

    # Jangan lupa untuk menambahkan baris terakhir
    if current_line:
        lines.append(current_line)

    return lines

# Fungsi untuk menghasilkan kombinasi berdasarkan kategori
def generate_combinations_by_category(aksara, sandhangan, aksara_tumpuk, aksara_khusus, simbol, swara, angka):
    results = {
        "tanpa_sandhangan": [],
        "dengan_sandhangan": [],
        "tumpuk": [],
        "tumpuk_dengan_sandhangan": [],
        "tumpuk_khusus": [],
        "tumpuk_khusus_dengan_sandhangan": [],
        "dengan_swara": [],  # Tambahkan kategori untuk swara
        "dengan_simbol": [],
        "dengan_angka": [],
        "dengan_spesial": [],
        "dengan_tumpuk_spesial": []
    }

    for a in aksara:
        # Kombinasi aksara tanpa sandhangan
        results["tanpa_sandhangan"].append(a)

        # Kombinasi aksara dengan sandhangan
        sandhangan_combination = ''.join([a + s + " " for s in sandhangan])
        results["dengan_sandhangan"].append(sandhangan_combination)

        # Kombinasi aksara dengan tumpukan
        tumpuk_combination = ''.join([a + t + " " for t in aksara_tumpuk])
        results["tumpuk"].append(tumpuk_combination)

        # Kombinasi aksara dengan tumpukan dan sandhangan
        tumpuk_sandhangan_combination = ''.join([a + t + s + " " for t in aksara_tumpuk for s in sandhangan])
        results["tumpuk_dengan_sandhangan"].append(tumpuk_sandhangan_combination)

        # Kombinasi aksara dengan tumpukan khusus
        tumpuk_khusus_combination = ''.join([a + k + " " for k in aksara_khusus])
        results["tumpuk_khusus"].append(tumpuk_khusus_combination)

        # Kombinasi aksara dengan tumpukan khusus dan sandhangan
        tumpuk_khusus_sandhangan_combination = ''.join([a + k + s + " " for k in aksara_khusus for s in sandhangan])
        results["tumpuk_khusus_dengan_sandhangan"].append(tumpuk_khusus_sandhangan_combination)

        # Kombinasi aksara dengan swara
        swara_combination = ''.join([a + S + " " for S in swara])
        results["dengan_swara"].append(swara_combination)

        # Kombinasi swara dengan simbol
        simbol_combination = ''.join([a + M + " " for M in simbol])
        results["dengan_simbol"].append(simbol_combination)
        
        # Kombinasi swara dengan angka
        angka_combination = ''.join([a + A + " " for A in angka])
        results["dengan_angka"].append(angka_combination)

        # Kombinasi spesial
        spesial_combination = ''.join([a + x + " " for x in aksara_spesial])
        results["dengan_spesial"].append(spesial_combination)

        # Kombinasi tumpuk dengan spesial
        #spesial_tumpuk_combination = ''.join([a + t + x + " " for t in aksara_tumpuk for x in aksara_spesial])
        #results["dengan_tumpuk_spesial"].append(spesial_tumpuk_combination)        

    # Gabungkan semua aksara tanpa sandhangan dalam satu baris
    results["tanpa_sandhangan"] = [''.join(results["tanpa_sandhangan"])]

    # Pecah setiap kombinasi menjadi baris-baris dengan panjang maksimal 20 karakter
    for category in results:
        results[category] = sum([split_into_lines(combination) for combination in results[category]], [])

    return results

# Hasilkan semua kombinasi
combinations_by_category = generate_combinations_by_category(aksara_jawa, sandhangan, aksara_tumpuk, aksara_khusus, swara, simbol, angka)

# Simpan hasil ke satu file dengan pemisah antar kategori
with open('sample_text_jawa/kombinasi_aksara_jawa.txt', 'w', encoding='utf-8') as file:
    for category, combinations in combinations_by_category.items():
        #file.write(f"\n=== {category.replace('_', ' ').upper()} ===\n")
        file.write('\n'.join(combinations) + '\n')

print("Kombinasi aksara Jawa telah disimpan ke dalam satu file dengan kategori terpisah dan format per aksara pada satu baris, dengan batas panjang baris 20 karakter.")
