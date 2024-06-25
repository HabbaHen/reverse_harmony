from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel

from src.desktop_application.CSS import CSS
from src.desktop_application.file_upload.FileUpload import FileUpload


class SaveFileButton(QWidget):

    DISABLED_STATE_TOOLTIP = "No input file chosen"

    def __init__(self, width, height):
        if width <= 5 or height <= 5:
            raise ValueError("Sizes of `Save file button` must be greater than 5")
        super().__init__()
        layout = QHBoxLayout()
        layout.addStretch(stretch=1)
        self.feedbackMessageLabel = QLabel()
        self.feedbackMessageLabel.hide()
        layout.addWidget(self.feedbackMessageLabel, stretch=0)
        self.saveFileButton = QPushButton()
        self.saveFileButton.setCursor(QCursor(Qt.PointingHandCursor))
        saveFileIcon = QIcon(":/resources/save-file.svg")
        self.saveFileButton.setIcon(saveFileIcon)
        self.saveFileButton.setIconSize(QSize(width, height))
        self.saveFileButton.setFixedSize(width, height)
        layout.addWidget(self.saveFileButton, stretch=0)
        self.setLayout(layout)
        self.saveFileButton.clicked.connect(self.onSaveFileButtonClicked)

    def initializeState(self):
        self.setDisabledState()

    def setDisabledState(self):
        self.hideFeedbackMessage()
        self.saveFileButton.setDisabled(True)
        self.saveFileButton.setToolTip(self.DISABLED_STATE_TOOLTIP)

    def setDisabledStateWithTooltip(self, tooltipText):
        self.hideFeedbackMessage()
        self.saveFileButton.setDisabled(True)
        self.saveFileButton.setToolTip(tooltipText)

    def setEnabledState(self):
        self.saveFileButton.setDisabled(False)
        self.saveFileButton.setToolTip("")

    def hideFeedbackMessage(self):
        self.feedbackMessageLabel.hide()

    def onSaveFileButtonClicked(self):
        self.hideFeedbackMessage()
        filename = FileUpload.chooseOutputFile("Save MP3 file as...")
        if not filename:
            return
        if not filename.endswith(".mp3"):
            filename = filename + ".mp3"
        with open(filename, "wb") as file:
            pass # todo - write
        pass # todo

    def _showSaveSuccessMessage(self):
        self.feedbackMessageLabel.setText("Save success")
        self.feedbackMessageLabel.setStyleSheet(CSS.SUCCESS_MESSAGE_STYLE)
        self.feedbackMessageLabel.show()

    def _showSaveFailureMessage(self):
        self.feedbackMessageLabel.setText("Save failure!")
        self.feedbackMessageLabel.setStyleSheet(CSS.ERROR_MESSAGE_STYLE)
        self.feedbackMessageLabel.show()
