from os import path

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton

import resources
from src.desktop_application.file_picker.FileDropLineEdit import FileDropLineEdit
from src.desktop_application.file_picker.FileDropOrPickArea import FileDropOrPickArea
from src.desktop_application.file_upload.FileUpload import FileUpload


class InputFilePicker(QWidget):

    def __init__(self, maxFileNameLengthShown, height):
        super().__init__()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.fileDropArea = FileDropOrPickArea(self)
        self.chosenFileLabel = FileDropLineEdit(maxFileNameLengthShown, height)
        self.chosenFileLabel.setReadOnly(True)
        self.chosenFileLabel.hide()
        self.uploadButton = QPushButton()
        self.uploadButton.setIcon(QIcon(":/resources/icons/file-upload.svg"))
        self.uploadButton.setIconSize(QSize(30, height))
        self.uploadButton.setFixedSize(30, height)
        self.uploadButton.clicked.connect(self.onUploadButtonClicked)
        self.uploadButton.hide()
        self.crossButton = QPushButton("X")
        self.crossButton.setFixedSize(30, height)
        self.crossButton.clicked.connect(self.onCrossButtonClicked)
        self.crossButton.hide()
        self.label = QLabel("Input file: ")
        layout.addWidget(self.label, stretch=0)
        layout.addWidget(self.fileDropArea, stretch=1)
        layout.addWidget(self.chosenFileLabel, stretch=0)
        layout.addWidget(self.uploadButton, stretch=0)
        layout.addWidget(self.crossButton)
        self.errorMessageLabel = QLabel()
        self.errorMessageLabel.hide()
        layout.addWidget(self.errorMessageLabel, stretch=0)
        self.endWidget = QWidget()
        self.endWidget.hide()
        layout.addWidget(self.endWidget, stretch=1)
        self.setLayout(layout)

    def onCrossButtonClicked(self):
        self.chosenFileLabel.hide()
        self.uploadButton.hide()
        self.crossButton.hide()
        self.errorMessageLabel.hide()
        self.endWidget.hide()
        self.fileDropArea.show()

    def onUploadButtonClicked(self):
        filename = FileUpload.uploadInputFile("Upload Audio File")
        if filename and path.isfile(filename):
            self.chosenFileLabel.changeFilename(filename)
