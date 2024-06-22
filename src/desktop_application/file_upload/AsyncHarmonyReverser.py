from PyQt5.QtCore import QRunnable
from src.backend.HarmonyReverser import HarmonyReverser


class AsyncHarmonyReverser(QRunnable):

    def __init__(self, filePicker):
        super().__init__()
        self.filePicker = filePicker

    def run(self):
        filename = self.filePicker.chosenFileLabel.toolTip()
        harmonyReverser = HarmonyReverser(filename)
        if harmonyReverser.getErrorMessage() is not None:
            self._finish(harmonyReverser.getErrorMessage(), None)
            return
        reversedAudio = harmonyReverser.reverseHarmony()
        if harmonyReverser.getErrorMessage() is not None:
            self._finish(harmonyReverser.getErrorMessage(), None)
            return
        self._finish(None, reversedAudio)

    def _finish(self, errorMessage, result):
        self.filePicker.fileUploadResult = (errorMessage, result)
        self.filePicker.fileUploadFinished.emit()
