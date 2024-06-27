from os import path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QLabel

from src.desktop_application.EntryPoints import EntryPoints
from src.desktop_application.ResourcePaths import ResourcePaths


class FileDropOrPickArea(QLineEdit):

    def __init__(self, filePicker, height):
        if height <= 10:
            raise ValueError("height must be greater than 10 for FileDropOrPickArea")
        super().__init__()
        self.filePicker = filePicker
        self.setFixedHeight(height)
        self.setReadOnly(True)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        image = QPixmap(ResourcePaths.DRAG_AND_DROP_ICON).scaledToHeight(height - 15, Qt.SmoothTransformation)
        dragAndDropImage = QLabel()
        dragAndDropImage.setPixmap(image)
        layout.addWidget(dragAndDropImage)
        self.setLayout(layout)

    def changeFilename(self, filename):
        self.hide()
        self.filePicker.chosenFileLabel.show()
        self.filePicker.crossButton.show()
        self.filePicker.endWidget.show()
        self.filePicker.chosenFileLabel.changeFilename(filename)
