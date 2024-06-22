from os import path
from PyQt5.QtWidgets import QLineEdit


class FileDropOrPickArea(QLineEdit):

    def __init__(self, filePicker):
        super().__init__()
        self.filename = None
        self.filePicker = filePicker
        # todo

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
                self._changeFilename(file)
            event.acceptProposedAction()

    def _changeFilename(self, filename):
        self.filePicker.chosenFileLabel.changeFilename(filename)
        self.hide()
        self.filePicker.errorMessageLabel.hide()
        self.filePicker.chosenFileLabel.show()
        self.filePicker.uploadButton.show()
        self.filePicker.crossButton.show()
        self.filePicker.endWidget.show()
