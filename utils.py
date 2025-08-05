import cv2
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap

def apply_filter(frame, filter_type):
    if filter_type == "vintage":
        # Apply a sepia-tone effect
        kernel = cv2.transform(frame, 
            cv2.COLOR_BGR2RGB) * [0.393, 0.769, 0.189] + \
            cv2.transform(frame, cv2.COLOR_BGR2RGB) * [0.349, 0.686, 0.168] + \
            cv2.transform(frame, cv2.COLOR_BGR2RGB) * [0.272, 0.534, 0.131]
        sepia = cv2.transform(frame, kernel.astype("float32"))
        return cv2.convertScaleAbs(sepia)
    return frame

def add_sticker_overlay(frame, sticker_type):
    try:
        sticker_path = f"assets/stickers/{sticker_type}.png"
        sticker = cv2.imread(sticker_path, cv2.IMREAD_UNCHANGED)

        if sticker is None:
            return frame

        # Resize sticker to fit face area (just example: place at top left)
        sticker = cv2.resize(sticker, (100, 100))

        # Get region of interest
        y1, y2 = 20, 120
        x1, x2 = 20, 120

        alpha_s = sticker[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        for c in range(3):
            frame[y1:y2, x1:x2, c] = (alpha_s * sticker[:, :, c] +
                                      alpha_l * frame[y1:y2, x1:x2, c])
    except:
        pass
    return frame

def show_countdown(label):
    def update_number(i):
        label.setText(str(i))
        QApplication.processEvents()
        time.sleep(1)

    for i in [3, 2, 1]:
        update_number(i)
    label.setText("📸")
    QApplication.processEvents()
    time.sleep(0.5)
    label.setText("")
