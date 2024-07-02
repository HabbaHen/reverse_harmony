import math

from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtGui import QPixmap, QCursor, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget, QPushButton, QSlider, QLabel, QHBoxLayout

from src.desktop_application.CSS import CSS
from src.desktop_application.EntryPoints import EntryPoints
from src.desktop_application.ResourcePaths import ResourcePaths
from src.desktop_application.audio_preview_player.AudioTimer import AudioTimer


class AudioPreviewPlayer(QWidget):

    DEBUG_MODE = False

    def __init__(self, height):
        super().__init__()
        self.playButton = QPushButton()
        self.playButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.playButton.setStyleSheet(CSS.AUDIO_PLAYER_BUTTON_STYLE)
        self.playButton.setIcon(QIcon(ResourcePaths.PLAY_AUDIO_BUTTON_ICON))
        self.playButton.setIconSize(QSize(height, height))
        self.playButton.setFixedSize(height, height)
        self.playButton.clicked.connect(self.onPlayButtonClicked)
        self.pausedButton = QPushButton()
        self.pausedButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pausedButton.setStyleSheet(CSS.AUDIO_PLAYER_BUTTON_STYLE)
        self.pausedButton.setIcon(QIcon(ResourcePaths.PAUSE_AUDIO_BUTTON_ICON))
        self.pausedButton.setIconSize(QSize(height, height))
        self.pausedButton.setFixedSize(height, height)
        self.pausedButton.clicked.connect(self.onPauseButtonClicked)
        self.audioTimeSlider = QSlider(Qt.Horizontal)
        self.audioTimeSlider.setCursor(QCursor(Qt.PointingHandCursor))
        self.audioTimeSlider.setFixedHeight(height)
        self.audioTimeSlider.setMinimumWidth(220)
        self.audioTimeSlider.setMinimum(0)
        self.audioTimeSlider.setMaximum(100000)
        self.audioTimeSlider.setValue(0)
        self.audioTimeSlider.setPageStep(5000)
        self.audioTimeSlider.valueChanged.connect(self.onAudioTimeSliderChanged)
        self.currentTimeLabel = QLabel()
        self.currentTimeLabel.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.currentTimeLabel.setMinimumWidth(50)
        self.currentTimeLabel.setFixedHeight(height)
        self.totalTimeLabel = QLabel()
        self.totalTimeLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.totalTimeLabel.setMinimumWidth(50)
        self.totalTimeLabel.setFixedHeight(height)
        self.audioTimer = AudioTimer(self.currentTimeLabel, self.totalTimeLabel)
        self.volumeIcon = QLabel()
        self.volumeIcon.setPixmap(QPixmap(ResourcePaths.AUDIO_VOLUME_ICON)
                                  .scaledToHeight(height, Qt.SmoothTransformation))
        self.volumeSlider = QSlider(Qt.Horizontal)
        self.volumeSlider.setCursor(QCursor(Qt.PointingHandCursor))
        self.volumeSlider.setFixedHeight(height)
        self.volumeSlider.setFixedWidth(100)
        self.volumeSlider.setMinimum(0)
        self.volumeSlider.setMaximum(1000)
        self.volumeSlider.setValue(500)
        self.volumeSlider.setPageStep(100)
        self.volumeSlider.valueChanged.connect(self.onVolumeSliderChanged)
        layout = QHBoxLayout()
        layout.addWidget(self.playButton, stretch=0)
        layout.addWidget(self.pausedButton, stretch=0)
        layout.addWidget(self.currentTimeLabel, stretch=0)
        layout.addWidget(self.audioTimeSlider, stretch=1)
        layout.addWidget(self.totalTimeLabel, stretch=0)
        layout.addWidget(self.volumeIcon, stretch=0)
        layout.addWidget(self.volumeSlider, stretch=0)
        self.setLayout(layout)
        self._audioPlayersGroups = []
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.mediaStatusChanged.connect(self.onMediaStatusChanged)
        self.audioDuration = 0
        self.clearAudioFromPlayer()
        self.mediaPlayer.positionChanged.connect(self.onMediaPositionChanged)

    def addToGroup(self, audioPlayersGroup):
        self._audioPlayersGroups.append(audioPlayersGroup)

    def onMediaStatusChanged(self, mediaStatus):
        if self.DEBUG_MODE:
            print("Media status changed | " + self._getMediaStatus(mediaStatus))
        if mediaStatus == QMediaPlayer.EndOfMedia:
            self.onPauseButtonClicked()

    def onMediaPositionChanged(self, audioPosition):
        if self.DEBUG_MODE:
            print("Media position changed | " + self._getMediaStatus(self.mediaPlayer.mediaStatus()))
        self._blockAllSignals()
        mediaDuration = self.audioDuration
        if mediaDuration == 0:
            return
        sliderPosition = math.floor((audioPosition / mediaDuration) * self.audioTimeSlider.maximum())
        if audioPosition == mediaDuration:
            sliderPosition = self.audioTimeSlider.maximum()
        self.audioTimeSlider.setValue(sliderPosition)
        timerCurrentSeconds = audioPosition // 1000
        self.audioTimer.setCurrentTime(timerCurrentSeconds)
        self._unblockAllSignals()

    def onPlayButtonClicked(self):
        if self.DEBUG_MODE:
            print("Play button clicked")
        self._blockAllSignals()
        for playersGroup in self._audioPlayersGroups:
            playersGroup.pauseAllAudioPlayers()
        self.playButton.hide()
        self.pausedButton.show()
        startAudioPosition = math.floor((self.audioTimeSlider.value() / self.audioTimeSlider.maximum()) * self.audioDuration)
        if self.audioTimeSlider.value() == self.audioTimeSlider.maximum():
            startAudioPosition = self.audioDuration
        self.mediaPlayer.setPosition(startAudioPosition)
        self.mediaPlayer.play()
        self._unblockAllSignals()

    def onPauseButtonClicked(self):
        if self.DEBUG_MODE:
            print("Pause button clicked")
        self._blockAllSignals()
        self.pausedButton.hide()
        self.playButton.show()
        self.mediaPlayer.pause()
        self.updateAudioTimers()
        self._unblockAllSignals()

    def updateAudioTimers(self):
        if self.DEBUG_MODE:
            print("Updating audio timers")
        self._blockAllSignals()
        mediaPosition = self.mediaPlayer.position()
        mediaDuration = self.audioDuration
        sliderPosition = math.floor((mediaPosition / mediaDuration) * self.audioTimeSlider.maximum())
        if mediaPosition == mediaDuration:
            sliderPosition = self.audioTimeSlider.maximum()
        self.audioTimeSlider.setValue(sliderPosition)
        timerCurrentSeconds = mediaPosition // 1000
        self.audioTimer.setCurrentTime(timerCurrentSeconds)
        self._unblockAllSignals()

    def onAudioTimeSliderChanged(self, changedValue):
        if self.DEBUG_MODE:
            print("Audio time slider changed")
        self._blockAllSignals()
        if self.mediaPlayer.mediaStatus() == QMediaPlayer.NoMedia:
            return
        updatedPosition = math.floor((changedValue / self.audioTimeSlider.maximum()) * self.audioDuration)
        if changedValue == self.audioTimeSlider.maximum():
            updatedPosition = self.audioDuration
        self.mediaPlayer.setPosition(updatedPosition)
        timerCurrentSeconds = updatedPosition // 1000
        self.audioTimer.setCurrentTime(timerCurrentSeconds)
        self._unblockAllSignals()

    def onVolumeSliderChanged(self, changedValue):
        if self.DEBUG_MODE:
            print("Volume slider changed")
        self._blockAllSignals()
        updateVolume = math.floor((changedValue / self.volumeSlider.maximum()) * 100)
        if changedValue == self.volumeSlider.maximum():
            updateVolume = 100
        self.mediaPlayer.setVolume(updateVolume)
        self._unblockAllSignals()

    def setAudioForPlayer(self, audioFile, audioLength, autoplay):
        if self.DEBUG_MODE:
            print("Set audio for player")
        self._blockAllSignals()
        self.audioDuration = math.floor(audioLength * 1000)
        self.mediaPlayer.stop()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(audioFile)))
        self.playButton.setDisabled(False)
        self.pausedButton.setDisabled(False)
        self.pausedButton.hide()
        self.audioTimeSlider.setDisabled(False)
        audioVolume = math.floor((self.volumeSlider.value() / self.volumeSlider.maximum()) * 100)
        if self.volumeSlider.value() == self.volumeSlider.maximum():
            audioVolume = 100
        self.audioTimer.setCurrentAndTotalTimes(0, self.audioDuration // 1000)
        self.updateAudioTimers()
        self.mediaPlayer.setVolume(audioVolume)
        self.mediaPlayer.setPosition(0)
        settingsPanel = EntryPoints.MAIN_WINDOW.outputModeSettingsPanel
        if settingsPanel.getStartAheadIsTurnedOn():
            self.mediaPlayer.setPosition(min(10_000, self.audioDuration // 3))
            self.updateAudioTimers()
        if settingsPanel.getAutoPlayIsTurnedOn() and autoplay:
            self.playButton.hide()
            self.pausedButton.show()
            self.mediaPlayer.play()
        self._unblockAllSignals()

    def clearAudioFromPlayer(self):
        if self.DEBUG_MODE:
            print("Cleared audio from player")
        self._blockAllSignals()
        self.mediaPlayer.stop()
        self.mediaPlayer.setMedia(QMediaContent())
        self.playButton.setDisabled(True)
        self.playButton.show()
        self.pausedButton.setDisabled(True)
        self.pausedButton.hide()
        self.audioTimeSlider.setDisabled(True)
        self.audioTimeSlider.setValue(0)
        self.audioTimer.setNoAudioState()
        self._unblockAllSignals()

    def _blockAllSignals(self):
        self.mediaPlayer.blockSignals(True)
        self.audioTimeSlider.blockSignals(True)

    def _unblockAllSignals(self):
        self.mediaPlayer.blockSignals(False)
        self.audioTimeSlider.blockSignals(False)

    def _getMediaStatus(self, mediaStatus):
        newStatus = "Unknown Status!"
        if mediaStatus == QMediaPlayer.UnknownMediaStatus:
            newStatus = "UnknownMediaStatus"
        elif mediaStatus == QMediaPlayer.NoMedia:
            newStatus = "NoMedia"
        elif mediaStatus == QMediaPlayer.LoadingMedia:
            newStatus = "LoadingMedia"
        elif mediaStatus == QMediaPlayer.LoadedMedia:
            newStatus = "LoadedMedia"
        elif mediaStatus == QMediaPlayer.StalledMedia:
            newStatus = "StalledMedia"
        elif mediaStatus == QMediaPlayer.BufferedMedia:
            newStatus = "BufferingMedia"
        elif mediaStatus == QMediaPlayer.BufferedMedia:
            newStatus = "BufferedMedia"
        elif mediaStatus == QMediaPlayer.EndOfMedia:
            newStatus = "EndOfMedia"
        elif mediaStatus == QMediaPlayer.InvalidMedia:
            newStatus = "InvalidMedia"
        return newStatus