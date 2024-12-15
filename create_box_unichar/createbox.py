from PIL import Image, ImageDraw, ImageFont
import unicodedata
import sys
import os

# Normalize text to NFC
def normalize_text(text):
    return unicodedata.normalize("NFC", text)

def create_box_file(text, font_path, output_image_path, output_box_path):
    font_size = 32
    try:
        font = ImageFont.truetype(font_path, font_size)
    except OSError:
        print(f"Error: Font file not found at {font_path}")
        sys.exit(1)

    image_width = 3600
    image_height = 480

    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    x, y = 10, 32
    box_data = []
    for char in text:
        bbox = draw.textbbox((x, y), char, font=font)
        if bbox is None:  # Handle invalid bounding box
            print(f"Warning: Unable to render character '{char}'")
            continue

        char_width = bbox[2] - bbox[0]
        char_height = bbox[3] - bbox[1]

        draw.text((x, y), char, font=font, fill="black")

        left = x
        bottom = image_height - y
        right = x + char_width
        top = image_height - (y + char_height)
        box_data.append(f"{char} {left} {top} {right} {bottom} 0")

        x += char_width

    image.save(output_image_path)

    with open(output_box_path, "w", encoding="utf-8") as box_file:
        box_file.write("\n".join(box_data))

    print(f"Box file saved to {output_box_path}")

def create_unicharset(text, output_unicharset_path):
    unique_chars = sorted(set(text))

    with open(output_unicharset_path, "w", encoding="utf-8") as unicharset_file:
        for char in unique_chars:
            unicode_val = ord(char)
            properties = "0 0,0,0,0 0"
            unicharset_file.write(f"{char} {properties} {unicode_val}\n")

    print(f"Unicharset file saved to {output_unicharset_path}")

if __name__ == "__main__":
    text_path = "langdata/lat_java.sample_text"
    font_path = "create_box_unichar/ramayana 4.12.ttf"
    output_dir = "create_box_unichar"

    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(text_path):
        print(f"Error: Text file not found at {text_path}")
        sys.exit(1)

    with open(text_path, "r", encoding="utf-8") as file:
        text = file.read().strip()

    # Normalize text for proper rendering
    text = normalize_text(text)

    output_image_path = os.path.join(output_dir, "output_image.tif")
    output_box_path = os.path.join(output_dir, "output.box")
    output_unicharset_path = os.path.join(output_dir, "output.unicharset")

    create_box_file(text, font_path, output_image_path, output_box_path)
    create_unicharset(text, output_unicharset_path)
