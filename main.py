from PyQt6.QtWidgets import QApplication, QStackedWidget, QPushButton, QVBoxLayout, QWidget
import sys
from camera_widget import CameraWidget
from gallery_widget import GalleryWidget

app = QApplication(sys.argv)
stack = QStackedWidget()

camera = CameraWidget(stack)
gallery = GalleryWidget()

stack.addWidget(camera)
stack.addWidget(gallery)
stack.setCurrentWidget(camera)
container = QWidget()
layout = QVBoxLayout()
layout.addWidget(stack)
container.setLayout(layout)

container.setWindowTitle("VibeCam by Aiman Ijaz📸")
container.resize(420, 720)
container.show()

sys.exit(app.exec())
