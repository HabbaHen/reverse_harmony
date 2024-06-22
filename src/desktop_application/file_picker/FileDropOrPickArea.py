from os import path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QLabel


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
        image = QPixmap(":/resources/drag-and-drop.svg").scaledToHeight(height - 10, Qt.SmoothTransformation)
        dragAndDropImage = QLabel()
        dragAndDropImage.setPixmap(image)
        layout.addWidget(dragAndDropImage)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        md = event.mimeData()
        if md.hasUrls():
            file = None
            for url in md.urls():
                if url.isLocalFile():
                    localFile = url.toLocalFile()
                    if path.isfile(localFile):
                        file = url.toLocalFile()
            if file is not None:
                self.changeFilename(file)
            event.acceptProposedAction()

    def changeFilename(self, filename):
        self.hide()
        self.filePicker.errorMessageLabel.hide()
        self.filePicker.chosenFileLabel.show()
        self.filePicker.crossButton.show()
        self.filePicker.endWidget.show()
        self.filePicker.chosenFileLabel.changeFilename(filename)
