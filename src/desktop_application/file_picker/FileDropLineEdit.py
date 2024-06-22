from os import path
from PyQt5.QtWidgets import QLineEdit


class FileDropLineEdit(QLineEdit):

    def __init__(self, maxLength, height, filePicker):
        if maxLength <= 5:
            raise ValueError("maxLength must be greater than 5 for FileDropLineEdit")
        super().__init__()
        self.filename = None
        self.maxLen = maxLength
        self.setText("")
        self.setToolTip("")
        self.setMinimumHeight(height)
        self.filePicker = filePicker

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        md = event.mimeData()
        if md.hasUrls():
            file = None
            for url in md.urls():
                localFile = url.toLocalFile()
                if localFile and path.isfile(localFile):
                    file = localFile
            if file is not None:
                self.changeFilename(file)
            event.acceptProposedAction()

    def changeFilename(self, filename):
        self.filename = filename
        displayedText = self.filename
        if len(self.filename) > self.maxLen:
            displayedText = "..." + self.filename[len(self.filename) - self.maxLen + 3:]
            slashPosition = displayedText.find("/")
            if slashPosition != -1:
                displayedText = "..." + displayedText[slashPosition:]
        self.setText(displayedText)
        self._resizeLineEditOfChosenFile(displayedText)
        self.setToolTip(self.filename)
        self.filePicker.onFileUploadStart()

    def _resizeLineEditOfChosenFile(self, displayedText):
        fontMetrics = self.fontMetrics()
        adjustedWidth = fontMetrics.horizontalAdvance(displayedText)
        self.setFixedWidth(adjustedWidth + 10)
