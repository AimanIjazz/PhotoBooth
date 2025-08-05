import os
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QScrollArea, QPushButton, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class GalleryWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.container = QWidget()
        self.inner_layout = QVBoxLayout()
        self.container.setLayout(self.inner_layout)
        scroll.setWidget(self.container)
        layout.addWidget(scroll)
        back_btn = QPushButton("🔙 Back")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)
        self.setLayout(layout)

    def go_back(self):
        self.parent().setCurrentIndex(0)

    def load_images(self):
        while self.inner_layout.count():
            child = self.inner_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        directory = "assets/captured"
        if not os.path.exists(directory):
            os.makedirs(directory)
        for filename in sorted(os.listdir(directory), reverse=True):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(directory, filename)
                pixmap = QPixmap(full_path).scaledToWidth(300, Qt.TransformationMode.SmoothTransformation)
                img_label = QLabel()
                img_label.setPixmap(pixmap)
                delete_btn = QPushButton("🗑 Delete")
                delete_btn.clicked.connect(lambda _, f=full_path: self.delete_image(f))
                row = QHBoxLayout()
                row.addWidget(img_label)
                row.addWidget(delete_btn)
                row_widget = QWidget()
                row_widget.setLayout(row)
                self.inner_layout.addWidget(row_widget)

    def delete_image(self, filepath):
        reply = QMessageBox.question(self, "Delete Image", "Are you sure you want to delete this image?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes and os.path.exists(filepath):
            os.remove(filepath)
            self.load_images()
