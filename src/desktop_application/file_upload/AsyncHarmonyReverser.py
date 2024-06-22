import time

from PyQt5.QtCore import QRunnable, QThread


class AsyncHarmonyReverser(QRunnable):

    def __init__(self, filePicker):
        super().__init__()
        self.filePicker = filePicker

    def run(self):
        time.sleep(5) # todo - harmony reverse here
        # todo - move below code to be executed by main thread
        self.filePicker.uploadButton.setDisabled(False)
        self.filePicker.crossButton.setDisabled(False)
        self.filePicker.chosenFileLabel.setDisabled(False)
        self.filePicker.fileDropArea.setDisabled(False)
        self.filePicker.loadingLabel.hide()
        self.filePicker.loadingGif.stop()
