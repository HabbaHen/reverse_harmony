from PyQt5.QtCore import QRunnable
from src.backend.HarmonyReverser import HarmonyReverser
from src.desktop_application.EntryPoints import EntryPoints


class AsyncHarmonyReverser(QRunnable):

    def __init__(self, filePicker):
        super().__init__()
        self.filePicker = filePicker

    def run(self):
        filename = EntryPoints.MAIN_WINDOW.getCurrentlyChosenFilename()
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
        self._finish(None, originalAudio, reversedAudio, harmonyReverser.getAudioLengthInSeconds())

    def _finish(self, errorMessage, originalAudio, reversedAudio, audioLength):
        self.filePicker.fileUploadResult = (errorMessage, originalAudio, reversedAudio, audioLength)
        self.filePicker.fileUploadFinished.emit()
