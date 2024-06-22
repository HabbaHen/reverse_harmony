from os import path

from PyQt5.QtWidgets import (QWidget, QMainWindow, QPushButton, QVBoxLayout)
from src.desktop_application.OutputModeSettingsPanel import OutputModeSettingsPanel
from src.desktop_application.file_picker.InputFilePicker import InputFilePicker


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.inputFilePicker = InputFilePicker(70, 50)
        layout.addWidget(self.inputFilePicker, stretch=0)
        layout.addWidget(OutputModeSettingsPanel(), stretch=0)
        testButton = QPushButton('Bottom')
        testButton.setFlat(True)
        layout.addWidget(QPushButton('Bottom'), stretch=0)
        layout.addStretch(stretch=1)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(layout)
        self.resize(640, 400)
