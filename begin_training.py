import os
import subprocess

def run_tesseract_training(tessdata_prefix="../tesseract/tessdata", 
                           model_name="", 
                           start_model="", 
                           tessdata="../tesseract/tessdata", 
                           max_iterations=100):
    """
    Menjalankan command untuk training Tesseract dengan parameter yang dapat diubah.

    :param tessdata_prefix: Path ke direktori tessdata
    :param model_name: Nama model baru yang akan dibuat
    :param start_model: Model awal yang digunakan sebagai dasar
    :param tessdata: Path ke direktori tessdata
    :param max_iterations: Jumlah iterasi maksimum untuk pelatihan
    """
    # Pastikan berada di direktori `tesstrain`
    tesstrain_dir = "tesstrain"
    if not os.path.exists(tesstrain_dir):
        raise FileNotFoundError(f"Direktori '{tesstrain_dir}' tidak ditemukan.")
    os.chdir(tesstrain_dir)
    
    # Validasi path tessdata
    if not os.path.exists(tessdata_prefix):
        raise FileNotFoundError(f"Path tessdata_prefix '{tessdata_prefix}' tidak ditemukan.")
    if not os.path.exists(tessdata):
        raise FileNotFoundError(f"Path tessdata '{tessdata}' tidak ditemukan.")

    # Build command
    command = [
        "make", "training",
        f"MODEL_NAME={model_name}",
        f"START_MODEL={start_model}",
        f"TESSDATA={tessdata}",
        f"MAX_ITERATIONS={max_iterations}"
    ]

    # Menambahkan environment variable
    env = os.environ.copy()
    env["TESSDATA_PREFIX"] = tessdata_prefix

    try:
        # Jalankan command menggunakan subprocess
        result = subprocess.run(command, shell=False, check=True, text=True, env=env)
        print("Training berhasil dijalankan.")
        print("Output:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Terjadi kesalahan saat menjalankan training.")
        print("Error:")
        print(e.stderr)

# Contoh penggunaan
if __name__ == "__main__":
    try:
        run_tesseract_training(
            tessdata_prefix="/Users/geshamahendra/My_Home/ocr_tesseract/tesseract/tessdata",
            model_name="Jawa",
            start_model="Khmer",
            tessdata="/Users/geshamahendra/My_Home/ocr_tesseract/tesseract/tessdata",
            max_iterations=20000
        )
    except KeyboardInterrupt:
        print("\nProses dihentikan oleh pengguna.")
