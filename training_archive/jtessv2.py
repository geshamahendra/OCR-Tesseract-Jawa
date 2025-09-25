from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QWidget, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QListWidget, QSplitter, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QStatusBar
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image
import os
import sys

class VSCodeStyleEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TessBox Editor - VSCode Style")
        self.setGeometry(100, 100, 1200, 800)
        self.initUI()

    def initUI(self):
        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Graphics view for image
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        layout.addWidget(self.graphics_view)

        # Text editor for ground truth
        self.gt_editor = QTextEdit()
        layout.addWidget(self.gt_editor)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Load Folder Button
        load_folder_action = QPushButton("Load Folder")
        load_folder_action.clicked.connect(self.load_working_folder)
        layout.addWidget(load_folder_action)

        # Save Changes Button
        save_action = QPushButton("Save Changes")
        save_action.clicked.connect(self.save_changes)
        layout.addWidget(save_action)

        self.working_folder = ""
        self.files = []

    def load_working_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Working Folder")
        if not folder_path:
            return

        self.working_folder = folder_path
        self.scene.clear()

        files = os.listdir(folder_path)
        for file in files:
            name, ext = os.path.splitext(file)
            if ext.lower() in {".tif", ".box", ".txt"}:
                item = QTreeWidgetItem([name])
                self.file_tree.addTopLevelItem(item)

    def load_selected_file(self, item):
        file_root = item.text(0)

        tif_path = os.path.join(self.working_folder, f"{file_root}.tif")
        box_path = os.path.join(self.working_folder, f"{file_root}.box")
        gt_path = os.path.join(self.working_folder, f"{file_root}.gt.txt")

        if os.path.exists(tif_path) and os.path.exists(box_path) and os.path.exists(gt_path):
            self.load_image_and_boxes(tif_path, box_path)

            with open(gt_path, "r") as file:
                self.gt_editor.setText(file.read())

    def load_image_and_boxes(self, image_path, box_path):
        # Load image
        image = Image.open(image_path)
        if image.mode != "RGB":
            image = image.convert("RGB")
        pixmap = QPixmap.fromImage(QImage(image.tobytes(), image.width, image.height, QImage.Format_RGB888))
        self.scene.clear()
        self.scene.addPixmap(pixmap)

        # Load bounding boxes
        with open(box_path, "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 6:
                    char, x1, y1, x2, y2, _ = parts
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    rect_item = QGraphicsRectItem(x1, image.height - y2, x2 - x1, y2 - y1)
                    rect_item.setPen(Qt.red)
                    self.scene.addItem(rect_item)

    def save_changes(self):
        if not self.working_folder:
            self.status_bar.showMessage("No working folder loaded.")
            return

        current_item = self.file_tree.currentItem()
        if not current_item:
            self.status_bar.showMessage("No file selected.")
            return

        file_root = current_item.text(0)
        gt_path = os.path.join(self.working_folder, f"{file_root}.gt.txt")

        with open(gt_path, "w") as file:
            file.write(self.gt_editor.toPlainText())
        self.status_bar.showMessage(f"Saved: {gt_path}")

    # Additional methods for box editing functionalities

    def add_box_editor(self):
        # Create box editor widget here
        pass

    def add_box_generator(self):
        # Create box generator widget here
        pass

# Run the application
app = QApplication(sys.argv)
window = VSCodeStyleEditor()
window.show()
sys.exit(app.exec_())
