import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QWidget, QGraphicsScene, QGraphicsView, QGraphicsRectItem
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt
from PIL import Image, ImageSequence

class TessBoxEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TessBoxEditor - Python Edition")
        self.setGeometry(100, 100, 1200, 800)
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        # Button to load files
        self.load_button = QPushButton("Load Image and Box File")
        self.load_button.clicked.connect(self.load_files)
        layout.addWidget(self.load_button)

        # Graphics view for image display
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        layout.addWidget(self.graphics_view)

        # Text editor for ground truth text
        self.gt_editor = QTextEdit()
        layout.addWidget(QLabel("Ground Truth Text Editor"))
        layout.addWidget(self.gt_editor)

        # Save button
        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.central_widget.setLayout(layout)

    def load_files(self):
        # Load image
        image_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.tif *.png *.jpg)")
        if not image_path:
            return

        # Load box file
        box_path, _ = QFileDialog.getOpenFileName(self, "Open Box File", "", "Box Files (*.box)")
        if not box_path:
            return

        # Load ground truth text
        gt_path, _ = QFileDialog.getOpenFileName(self, "Open Ground Truth File", "", "Text Files (*.gt.txt *.txt)")
        if gt_path:
            with open(gt_path, 'r') as file:
                self.gt_editor.setText(file.read())

        # Visualize the image
        self.load_image_and_boxes(image_path, box_path)

    def load_image_and_boxes(self, image_path, box_path):
        # Load image
        image = Image.open(image_path)
        if image.mode != "RGB":
            image = image.convert("RGB")
        pixmap = QPixmap.fromImage(QImage(image.tobytes(), image.width, image.height, QImage.Format_RGB888))
        self.scene.clear()
        self.scene.addPixmap(pixmap)

        # Load and visualize bounding boxes
        with open(box_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 6:
                    char, x1, y1, x2, y2, _ = parts
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    rect_item = QGraphicsRectItem(x1, image.height - y2, x2 - x1, y2 - y1)
                    rect_item.setPen(Qt.red)
                    self.scene.addItem(rect_item)

    def save_changes(self):
        # Save ground truth text
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Ground Truth File", "", "Text Files (*.txt)")
        if save_path:
            with open(save_path, 'w') as file:
                file.write(self.gt_editor.toPlainText())
        print("Changes saved.")

# Run the application
app = QApplication(sys.argv)
window = TessBoxEditor()
window.show()
sys.exit(app.exec_())
