import time

from PyQt5.QtCore import QRunnable


class AsyncHarmonyReverser(QRunnable):

    def __init__(self, filePicker):
        super().__init__()
        self.filePicker = filePicker

    def run(self):
        time.sleep(1) # todo - harmony reverse here
        self.filePicker.fileUploadResult = ("TEST ERROR", None) # todo - (errorMessage, result)
        self.filePicker.fileUploadFinished.emit()
