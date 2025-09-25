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
    '', 'ꦴ', 'ꦶ', 'ꦷ', 'ꦸ', 'ꦹ', 'ꦼ', 'ꦺ', 'ꦺꦴ', 'ꦻꦴ', 'ꦀ', 'ꦁ', 'ꦂ', '꦳', 'ꦃ',
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
    '꧀ꦨ', '꧀ꦩ', '꧀ꦘ'
]

aksara_khusus = [
    'ꦾ', 'ꦿ', '꧀ꦮ'
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
        sandhangan_combination = ''.join([a + s + '꧈' for s in sandhangan])
        results["dengan_sandhangan"].append(sandhangan_combination)

        # Kombinasi aksara dengan tumpukan
        tumpuk_combination = ''.join([a + t + '꧈' for t in aksara_tumpuk])
        results["tumpuk"].append(tumpuk_combination)

        # Kombinasi aksara dengan tumpukan dan sandhangan
        tumpuk_sandhangan_combination = ''.join([a + t + s + '꧈' for t in aksara_tumpuk for s in sandhangan])
        results["tumpuk_dengan_sandhangan"].append(tumpuk_sandhangan_combination)

        # Kombinasi aksara dengan tumpukan khusus
        tumpuk_khusus_combination = ''.join([a + k + '꧈' for k in aksara_khusus])
        results["tumpuk_khusus"].append(tumpuk_khusus_combination)

        # Kombinasi aksara dengan tumpukan khusus dan sandhangan
        tumpuk_khusus_sandhangan_combination = ''.join([a + k + s + '꧈' for k in aksara_khusus for s in sandhangan])
        results["tumpuk_khusus_dengan_sandhangan"].append(tumpuk_khusus_sandhangan_combination)

    # Gabungkan semua aksara tanpa sandhangan dalam satu baris
    results["tanpa_sandhangan"] = [''.join(results["tanpa_sandhangan"])]

    return results

# Hasilkan semua kombinasi
combinations_by_category = generate_combinations_by_category(aksara_jawa, sandhangan, aksara_tumpuk, aksara_khusus)

# Simpan hasil ke satu file dengan pemisah antar kategori
with open('sample_text_jawa/kombinasi_aksara_jawa.txt', 'w', encoding='utf-8') as file:
    for category, combinations in combinations_by_category.items():
        file.write(f"\n=== {category.replace('_', ' ').upper()} ===\n")
        file.write('\n'.join(combinations) + '\n')

print("Kombinasi aksara Jawa telah disimpan ke dalam satu file dengan kategori terpisah dan format per aksara pada satu baris.")
