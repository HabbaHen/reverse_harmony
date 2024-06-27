from PyQt5.QtWidgets import QWidget, QVBoxLayout


class AudioPreviewPlayersGroup(QWidget):

    def __init__(self, audioPreviewPlayers):
        super().__init__()
        layout = QVBoxLayout()
        for audioPlayer in audioPreviewPlayers:
            layout.addWidget(audioPlayer)
            audioPlayer.addToGroup(self)
        self.setLayout(layout)
        self._audioPlayers = audioPreviewPlayers

    def pauseAllAudioPlayers(self):
        for audioPlayer in self._audioPlayers:
            audioPlayer.onPauseButtonClicked()

    def clearAudioFromAllAudioPlayers(self):
        for audioPlayer in self._audioPlayers:
            audioPlayer.clearAudioFromPlayer()
