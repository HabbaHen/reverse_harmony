from os import path

from PyQt5.QtWidgets import QWidget


class CentralWidget(QWidget):

    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        self.mainWindow.inputFilePicker.errorMessageLabel.hide()
        md = event.mimeData()
        if md.hasUrls():
            file = None
            for url in md.urls():
                localFile = url.toLocalFile()
                if localFile and path.isfile(localFile):
                    file = localFile
            if file is not None:
                self._changeFilename(file)
            event.acceptProposedAction()

    def _changeFilename(self, filename):
        if self.mainWindow.inputFilePicker.chosenFileLabel.isVisible():
            self.mainWindow.inputFilePicker.chosenFileLabel.changeFilename(filename)
        elif self.mainWindow.inputFilePicker.fileDropArea.isVisible():
            self.mainWindow.inputFilePicker.fileDropArea.changeFilename(filename)
