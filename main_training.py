import subprocess
import os

def run_tesseract_convert():
    # Set environment variable for TESSDATA_PREFIX
    os.environ["TESSDATA_PREFIX"] = "tesstrain/data/eng_jawa.traineddata"

    # Command to run
    command = [
        "make", "training",
        "START_MODEL=eng",
        "MODEL_NAME=eng_jawa",
        "TESSDATA=../tesseract/tessdata",
        "MAX_ITERATIONS=1000"
    ]

    try:
        # Run the command
        subprocess.run(command, check=True)
        print("Convert successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during convert: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    run_tesseract_convert()