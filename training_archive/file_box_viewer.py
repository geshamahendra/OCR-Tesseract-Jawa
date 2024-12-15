import matplotlib.pyplot as plt
from PIL import Image, ImageSequence

def parse_box_file(box_file_path):
    """
    Parse a .box file to extract character and bounding box information.
    """
    bounding_boxes = []
    with open(box_file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 6:
                char, x1, y1, x2, y2, page = parts
                bounding_boxes.append((char, int(x1), int(y1), int(x2), int(y2), int(page)))
    return bounding_boxes

def visualize_boxes_tiff(image_path, box_file_path):
    """
    Visualize bounding boxes from a .box file on multi-page TIFF image.
    """
    # Load bounding boxes and group by page
    bounding_boxes = parse_box_file(box_file_path)
    boxes_by_page = {}
    for box in bounding_boxes:
        char, x1, y1, x2, y2, page = box
        boxes_by_page.setdefault(int(page), []).append((char, x1, y1, x2, y2))
    
    # Open multi-page TIFF
    with Image.open(image_path) as img:
        for i, page in enumerate(ImageSequence.Iterator(img)):
            fig, ax = plt.subplots(figsize=(12, 8))
            ax.imshow(page, cmap="gray")

            # Draw bounding boxes for this page
            for char, x1, y1, x2, y2 in boxes_by_page.get(i, []):
                # Invert y-coordinates to match image coordinate system
                y1, y2 = page.size[1] - y1, page.size[1] - y2
                rect = plt.Rectangle((x1, y2), x2 - x1, y1 - y2, edgecolor='red', facecolor='none')
                ax.add_patch(rect)
                ax.text((x1 + x2) / 2, (y2 + y1) / 2, char, color='blue', fontsize=8, ha='center', va='center')

            ax.axis('off')
            plt.title(f"Page {i+1} - Bounding Box Visualization")
            plt.show()

# Example usage
image_path = "pdf_to_txt/training/training_data/line_1.tif"  # Replace with your TIFF image path
box_file_path = "pdf_to_txt/training/training_data/line_1.box"  # Replace with your box file path
visualize_boxes_tiff(image_path, box_file_path)
