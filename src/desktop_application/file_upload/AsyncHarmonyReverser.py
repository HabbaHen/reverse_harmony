import time

from PyQt5.QtCore import QRunnable


class AsyncHarmonyReverser(QRunnable):

    def __init__(self, filePicker):
        super().__init__()
        self.filePicker = filePicker

    def run(self):
        time.sleep(5) # todo - harmony reverse here
        self.filePicker.harmonyReverseResult = None # todo
        self.filePicker.fileUploadFinished.emit()
