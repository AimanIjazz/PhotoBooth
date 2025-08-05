import cv2
import os
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFileDialog, QMessageBox, QComboBox
)
from PyQt6.QtGui import QImage, QPixmap, QFont, QFontDatabase
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve
from utils import apply_filter, show_countdown


class CameraWidget(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.capture = cv2.VideoCapture(0)
        self.current_filter = "original"

        # Load custom font (e.g., Poppins)
        font_path = "assets/fonts/Poppins-Regular.ttf"
        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            app_font = QFont(family, 10)
            self.setFont(app_font)

        # Global pastel pink theme
        self.setStyleSheet("""
            QPushButton {
                background-color: #ffb6c1;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #ff99aa;
            }
            QComboBox {
                background-color: #fff0f5;
                border: 1px solid #ffc0cb;
                padding: 6px;
                border-radius: 5px;
            }
            QLabel {
                font-size: 14px;
                color: #d63384;
            }
        """)

        self.label = QLabel("Loading camera...")
        self.label.setFixedSize(380, 500)
        self.label.setStyleSheet("""
            border: 2px solid #ffc0cb;
            border-radius: 12px;
            background-color: #fff0f5;
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWindowOpacity(0.0)

        # Fade-in animation
        self.anim = QPropertyAnimation(self.label, b"windowOpacity")
        self.anim.setDuration(1500)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.anim.start()

        self.countdown_label = QLabel("")
        self.countdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.countdown_label.setStyleSheet("font-size: 48px; color: #ff69b4;")

        self.capture_btn = QPushButton("📸 Capture")
        self.capture_btn.clicked.connect(self.capture_image)

        self.gallery_btn = QPushButton("🖼 View Gallery")
        self.gallery_btn.clicked.connect(self.view_gallery)

        # Filter dropdown
        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItems(["original", "vintage", "grayscale", "blur", "negative", "cool", "warm"])
        self.filter_dropdown.currentTextChanged.connect(self.change_filter)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("🎨 Filter:"))
        filter_layout.addWidget(self.filter_dropdown)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.countdown_label)
        layout.addLayout(filter_layout)
        layout.addWidget(self.capture_btn)
        layout.addWidget(self.gallery_btn)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.capture.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)
        if self.current_filter != "original":
            frame = apply_filter(frame, self.current_filter)

        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if len(rgb_image.shape) == 2:
            rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_GRAY2RGB)

        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(q_img))

    def capture_image(self):
        show_countdown(self.countdown_label)
        ret, frame = self.capture.read()
        if not ret:
            return
        frame = cv2.flip(frame, 1)
        if self.current_filter != "original":
            frame = apply_filter(frame, self.current_filter)

        filename = QFileDialog.getSaveFileName(self, "Save Image", "assets/captured/photo.jpg", "Images (*.jpg)")[0]
        if filename:
            cv2.imwrite(filename, frame)
            QMessageBox.information(self, "Saved", "Image saved to gallery!")

    def view_gallery(self):
        self.stack.setCurrentIndex(1)
        self.stack.widget(1).load_images()

    def change_filter(self, selected_filter):
        self.current_filter = selected_filter
