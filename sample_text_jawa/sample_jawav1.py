# Daftar aksara Jawa dasar
aksara_jawa = [
    'ꦏ', 'ꦑ', 'ꦒ', 'ꦓ', 'ꦔ', 'ꦲ', 'ꦲ',
    'ꦕ', 'ꦖ', 'ꦗ', 'ꦙ', 'ꦚ', 'ꦯ',
    'ꦪ', 'ꦛ', 'ꦜ', 'ꦝ', 'ꦞ', 'ꦟ',
    'ꦰ', 'ꦫ', 'ꦠ', 'ꦡ', 'ꦢ', 'ꦣ',
    'ꦤ', 'ꦱ', 'ꦭ', 'ꦥ', 'ꦦ', 'ꦧ',
    'ꦨ', 'ꦩ', 'ꦮ', 'ꦘ'
]

# Daftar sandhangan
sandhangan = [
    '', 'ꦴ', 'ꦶ', 'ꦷ', 'ꦸ', 'ꦹ', 'ꦼ', 'ꦺ', 'ꦺꦴ', 'ꦻꦴ', 'ꦀ', 'ꦁ', 'ꦂ', '꦳', 'ꦃ'
    '꧊', '꧋', '꧌', '꧍', '꧁', '꧂', '꧃', '꧄', '꧅',
    '꧑', '꧒', '꧓', '꧔', '꧕', '꧖', '꧗', '꧘', '꧙', '꧐',
    '꧀', '꧉', '꧈', '꧇'
]

# Daftar aksara yang bisa ditumpuk
aksara_tumpuk = [
    '꧀ꦏ', '꧀ꦑ', '꧀ꦒ', '꧀ꦓ', '꧀ꦔ', '꧀ꦲ', '꧀ꦲ',
    '꧀ꦕ', '꧀ꦖ', '꧀ꦗ', '꧀ꦙ', '꧀ꦚ', '꧀ꦯ',
    '꧀ꦪ', '꧀ꦛ', '꧀ꦜ', '꧀ꦝ', '꧀ꦞ', '꧀ꦟ',
    '꧀ꦰ', '꧀ꦫ', '꧀ꦠ', '꧀ꦡ', '꧀ꦢ', '꧀ꦣ',
    '꧀ꦤ', '꧀ꦱ', '꧀ꦭ', '꧀ꦥ', '꧀ꦦ', '꧀ꦧ',
    '꧀ꦨ', '꧀ꦩ', '꧀ꦮ', '꧀ꦘ'
]

aksara_khusus = [
    'ꦾ', 'ꦿ', '꧀ꦮ', 'ꦫ꧀'
]

# Fungsi untuk menghasilkan kombinasi berdasarkan kategori
def generate_combinations_by_category(aksara, sandhangan, aksara_tumpuk, aksara_khusus):
    results = {
        "tanpa_sandhangan": [],
        "dengan_sandhangan": [],
        "tumpuk": [],
        "tumpuk_dengan_sandhangan": [],
        "tumpuk_khusus": [],
        "tumpuk_khusus_dengan_sandhangan": []
    }

    for a in aksara:
        # Kombinasi aksara tanpa sandhangan
        results["tanpa_sandhangan"].append(a + '꧈')

        # Kombinasi aksara dengan sandhangan
        for s in sandhangan:
            results["dengan_sandhangan"].append(a + s + '꧈')

        # Kombinasi aksara dengan tumpukan
        for t in aksara_tumpuk:
            results["tumpuk"].append(a + t + '꧈')

        # Kombinasi aksara dengan tumpukan dan sandhangan
        for t in aksara_tumpuk:
            for s in sandhangan:
                results["tumpuk_dengan_sandhangan"].append(a + t + s + '꧈')

        # Kombinasi aksara dengan tumpukan khusus
        for k in aksara_khusus:
            results["tumpuk_khusus"].append(a + k + '꧈')

        # Kombinasi aksara dengan tumpukan khusus dan sandhangan
        for k in aksara_khusus:
            for s in sandhangan:
                results["tumpuk_khusus_dengan_sandhangan"].append(a + k + s + '꧈')

    return results

# Hasilkan semua kombinasi
combinations_by_category = generate_combinations_by_category(aksara_jawa, sandhangan, aksara_tumpuk, aksara_khusus)


# Simpan hasil ke file berdasarkan kategori
for category, combinations in combinations_by_category.items():
    filename = f'sample_text_jawa/kombinasi_{category}.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join(combinations))

print("Kombinasi aksara Jawa telah disimpan ke dalam file berdasarkan kategori.")