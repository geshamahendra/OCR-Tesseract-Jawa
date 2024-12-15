from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFileDialog, QWidget, QGraphicsScene, QGraphicsView,
    QGraphicsRectItem, QTreeWidget, QTreeWidgetItem, QStatusBar, QSplitter
)
from PyQt5.QtGui import QPixmap, QImage, QPen
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsItem
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
        layout = QHBoxLayout(self.central_widget)

        # File navigation panel (sebelah kiri)
        self.file_tree = QTreeWidget()
        self.file_tree.setHeaderLabel("Files")
        self.file_tree.itemClicked.connect(self.load_selected_file)
        layout.addWidget(self.file_tree, 1)  # 1/3 dari lebar utama

        # Splitter untuk image viewer dan ground truth editor
        splitter = QSplitter(Qt.Vertical)

        # Graphics view untuk menampilkan gambar
        self.graphics_view = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphics_view.setScene(self.scene)
        splitter.addWidget(self.graphics_view)

        # Text editor untuk ground truth
        self.gt_editor = QTextEdit()
        splitter.addWidget(self.gt_editor)

        # Tambahkan splitter ke layout utama
        layout.addWidget(splitter, 3)  # 2/3 dari lebar utama

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Toolbar
        toolbar = self.addToolBar("Toolbar")
        load_folder_action = QPushButton("Load Folder")
        load_folder_action.clicked.connect(self.load_working_folder)
        toolbar.addWidget(load_folder_action)

        save_action = QPushButton("Save Changes")
        save_action.clicked.connect(self.save_changes)
        toolbar.addWidget(save_action)

        self.working_folder = ""
        self.files = []


    def load_working_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Working Folder")
        if not folder_path:
            return

        self.working_folder = folder_path
        self.file_tree.clear()

        # Find all files in the folder
        files = os.listdir(folder_path)
        files.sort()  # Sort the files alphabetically
        print("Sorted files:", files)  # Debug log

        file_groups = {}
        for file in files:
            name, ext = os.path.splitext(file)
            ext = ext.lower()  # Normalize extension case
            if ext in {".tif", ".box", ".txt"}:  # Check if file has a valid extension
                base_name = os.path.splitext(name)[0]  # Get base name without extension
                if base_name not in file_groups:
                    file_groups[base_name] = set()
                file_groups[base_name].add(ext)

        print("File groups found:", file_groups)  # Debug log

        for name, extensions in file_groups.items():
            if {".tif", ".box", ".txt"} <= extensions:
                print("Adding file group:", name)  # Debug log
                item = QTreeWidgetItem([name])
                self.file_tree.addTopLevelItem(item)

        if not self.file_tree.topLevelItemCount():
            print("No valid files found.")  # Debug log




    def load_selected_file(self, item):
        file_root = item.text(0)

        # Load corresponding files
        tif_path = os.path.join(self.working_folder, f"{file_root}.tif")
        box_path = os.path.join(self.working_folder, f"{file_root}.box")
        gt_path = os.path.join(self.working_folder, f"{file_root}.gt.txt")

        if os.path.exists(tif_path) and os.path.exists(box_path) and os.path.exists(gt_path):
            self.load_image_and_boxes(tif_path, box_path)

            # Load ground truth text
            with open(gt_path, "r") as file:
                self.gt_editor.setText(file.read())
            self.status_bar.showMessage(f"Loaded: {file_root}")

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

        # Save ground truth text
        with open(gt_path, "w") as file:
            file.write(self.gt_editor.toPlainText())
        self.status_bar.showMessage(f"Saved: {gt_path}")


# Run the application
app = QApplication(sys.argv)
window = VSCodeStyleEditor()
window.show()
sys.exit(app.exec_())
