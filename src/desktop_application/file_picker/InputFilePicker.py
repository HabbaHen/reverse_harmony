import time
from os import path

from PyQt5.QtCore import Qt, QSize, QThreadPool
from PyQt5.QtGui import QIcon, QCursor, QMovie
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton, QApplication

import resources
from src.desktop_application.file_picker.FileDropLineEdit import FileDropLineEdit
from src.desktop_application.file_picker.FileDropOrPickArea import FileDropOrPickArea
from src.desktop_application.file_upload.AsyncHarmonyReverser import AsyncHarmonyReverser
from src.desktop_application.file_upload.FileUpload import FileUpload


class InputFilePicker(QWidget):

    def __init__(self, maxFileNameLengthShown, height):
        super().__init__()
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        self.fileDropArea = FileDropOrPickArea(self, height)
        self.chosenFileLabel = FileDropLineEdit(maxFileNameLengthShown, height, self)
        self.chosenFileLabel.setReadOnly(True)
        self.chosenFileLabel.hide()
        self.uploadButton = QPushButton()
        self.uploadButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.uploadButton.setIcon(QIcon(":/resources/file-upload.svg"))
        self.uploadButton.setIconSize(QSize(30, height))
        self.uploadButton.setFixedSize(30, height)
        self.uploadButton.clicked.connect(self.onUploadButtonClicked)
        self.crossButton = QPushButton("X")
        self.crossButton.setCursor(QCursor(Qt.PointingHandCursor))
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
        self.loadingLabel = QLabel()
        self.loadingLabel.setFixedSize(height, height)
        self.loadingGif = QMovie(":/resources/loading.gif")
        self.loadingGif.setScaledSize(QSize(height, height))
        self.loadingLabel.setMovie(self.loadingGif)
        self.loadingGif.start()
        self.loadingLabel.hide()
        layout.addWidget(self.loadingLabel, stretch=0)
        self.endWidget = QWidget()
        self.endWidget.hide()
        layout.addWidget(self.endWidget, stretch=1)
        self.setLayout(layout)

    def onCrossButtonClicked(self):
        self.chosenFileLabel.hide()
        self.crossButton.hide()
        self.errorMessageLabel.hide()
        self.endWidget.hide()
        self.fileDropArea.show()

    def onUploadButtonClicked(self):
        filename = FileUpload.uploadInputFile("Upload Audio File")
        if filename and path.isfile(filename):
            if self.chosenFileLabel.isVisible():
                self.chosenFileLabel.changeFilename(filename)
            elif self.fileDropArea.isVisible():
                self.fileDropArea.changeFilename(filename)

    def onFileUpload(self):
        self.loadingLabel.show()
        self.uploadButton.setDisabled(True)
        self.crossButton.setDisabled(True)
        self.chosenFileLabel.setDisabled(True)
        self.fileDropArea.setDisabled(True)
        QThreadPool.globalInstance().start(AsyncHarmonyReverser(self))
