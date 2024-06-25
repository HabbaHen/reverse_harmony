import time

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
            self._finish(harmonyReverser.getErrorMessage(), None, None)
            return
        originalAudio = harmonyReverser.getOriginalAudioInMp3Format()
        if harmonyReverser.getErrorMessage() is not None:
            self._finish(harmonyReverser.getErrorMessage(), None, None)
            return
        reversedAudio = harmonyReverser.getReversedAudioInMp3Format()
        if harmonyReverser.getErrorMessage() is not None:
            self._finish(harmonyReverser.getErrorMessage(), None, None)
            return
        self._finish(None, originalAudio, reversedAudio)

    def _finish(self, errorMessage, originalAudio, reversedAudio):
        self.filePicker.fileUploadResult = (errorMessage, originalAudio, reversedAudio)
        self.filePicker.fileUploadFinished.emit()
