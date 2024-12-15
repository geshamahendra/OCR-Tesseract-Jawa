import subprocess
import os

def train_tesseract(lang, tif_file, box_file, output_dir, norm_mode=1):
    """
    Function to train Tesseract with a given .tif and .box file.

    Args:
        lang (str): The language code for the training (e.g., 'eng').
        tif_file (str): Path to the .tif file.
        box_file (str): Path to the .box file.
        output_dir (str): Directory to store training outputs.
        norm_mode (int): Normalization mode for unicharset_extractor (1, 2, or 3).

    Returns:
        None
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Step 1: Generate .tr file
        tr_file = os.path.join(output_dir, f"{lang}.tr")
        command_1 = [
            "tesseract", tif_file, os.path.join(output_dir, lang), "box.train"
        ]
        print("Running:", " ".join(command_1))
        subprocess.run(command_1, check=True)

        # Step 2: Generate unicharset
        unicharset_file = os.path.join(output_dir, "unicharset")
        command_2 = [
            "unicharset_extractor", f"--norm_mode={norm_mode}", box_file
        ]
        print("Running:", " ".join(command_2))
        subprocess.run(command_2, check=True)

        # Debug: Check if unicharset file is created
        if not os.path.exists(unicharset_file):
            print(f"Expected unicharset path: {unicharset_file}")
            raise FileNotFoundError(f"Unicharset file not created: {unicharset_file}")

        print(f"Unicharset file created successfully at: {unicharset_file}")

        # Step 3: Create font_properties (optional, if specific fonts are used)
        font_properties_file = os.path.join(output_dir, "font_properties")
        with open(font_properties_file, "w") as f:
            f.write("Tahoma 0 0 0 0 0")

        # Step 4: Train the shape clustering
        shape_file = os.path.join(output_dir, f"{lang}.shapetable")
        command_3 = [
            "shapeclustering", "-F", font_properties_file, "-U", unicharset_file, tr_file
        ]
        print("Running:", " ".join(command_3))
        subprocess.run(command_3, check=True)

        # Step 5: Train mftraining
        mftraining_output = os.path.join(output_dir, f"{lang}.unicharset")
        command_4 = [
            "mftraining", "-F", font_properties_file, "-U", unicharset_file, "-O",
            mftraining_output, tr_file
        ]
        print("Running:", " ".join(command_4))
        subprocess.run(command_4, check=True)

        # Validate mftraining output
        if not os.path.exists(mftraining_output):
            raise FileNotFoundError(f"mftraining output not created: {mftraining_output}")

        # Step 6: Train cntraining
        command_5 = [
            "cntraining", tr_file
        ]
        print("Running:", " ".join(command_5))
        subprocess.run(command_5, check=True)

        # Step 7: Combine results into .traineddata
        command_6 = [
            "combine_tessdata", f"{output_dir}/{lang}"
        ]
        print("Running:", " ".join(command_6))
        subprocess.run(command_6, check=True)

        print(f"Training complete. Trained data saved in {output_dir}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        print("Ensure all Tesseract training tools are installed and accessible.")
    except FileNotFoundError as e:
        print(f"Missing file error: {e}")
        print("Check if the necessary files are generated correctly.")

# Example usage
train_tesseract(
    lang="eng_jawa",
    tif_file="pdf_to_txt/jTessBoxEditor/Generated_Box/eng.tahoma.exp0.tif",
    box_file="pdf_to_txt/jTessBoxEditor/Generated_Box/eng.tahoma.exp0.box",
    output_dir="pdf_to_txt/output_training",
    norm_mode=1  # Adjust norm_mode as needed (1, 2, or 3)

)
