import math
import vlc
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QCursor, QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QSlider, QLabel, QHBoxLayout

from src.desktop_application.CSS import CSS
from src.desktop_application.EntryPoints import EntryPoints
from src.desktop_application.ResourcePaths import ResourcePaths
from src.desktop_application.audio_preview_player.AudioTimer import AudioTimer


class AudioPreviewPlayer(QWidget):

    DEBUG_MODE = True

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
        self._vlcInstance = vlc.Instance('--no-video')
        self.currentAudioTime = 0
        self.audioDuration = 0
        self.audioMedia = None
        self.mediaPlayer = None
        self.restartMediaPlayer()
        self.clearAudioFromPlayer()
        self.restartMediaPlayerAddEvents()

    def restartMediaPlayer(self):
        self.mediaPlayer = self._vlcInstance.media_player_new()
        if self.audioMedia is not None:
            self.mediaPlayer.set_media(self.audioMedia)
        audioVolume = math.floor((self.volumeSlider.value() / self.volumeSlider.maximum()) * 100)
        if self.volumeSlider.value() == self.volumeSlider.maximum():
            audioVolume = 100
        self.mediaPlayer.audio_set_volume(audioVolume)

    def restartMediaPlayerAddEvents(self):
        events = self.mediaPlayer.event_manager()
        events.event_attach(vlc.EventType.MediaPlayerEndReached, self.onMediaFinishedPlaying)
        events.event_attach(vlc.EventType.MediaPlayerTimeChanged, self.onMediaPositionChanged)

    def addToGroup(self, audioPlayersGroup):
        self._audioPlayersGroups.append(audioPlayersGroup)

    def onMediaFinishedPlaying(self, event):
        if self.DEBUG_MODE:
            print("Media finished playing")
        self.currentAudioTime = self.audioDuration
        self.restartMediaPlayer()
        self.onPauseButtonClicked()
        self.restartMediaPlayerAddEvents()
        self.audioTimeSlider.setDisabled(True)

    def onMediaPositionChanged(self, event):
        audioPosition = event.u.new_time
        self.currentAudioTime = audioPosition
        if self.DEBUG_MODE:
            print("Media position changed | New time is " + str(audioPosition))
            print("Current audio time " + str(self.mediaPlayer.get_time()))
            print("Current audio time in player " + str(self.currentAudioTime))
            print("Total audio time " + str(self.mediaPlayer.get_length()))
            print("Total audio time in player " + str(self.audioDuration))
        self._blockAllSignals()
        mediaDuration = self.audioDuration
        if mediaDuration == 0:
            self._unblockAllSignals()
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
        self.audioTimeSlider.setDisabled(False)
        for playersGroup in self._audioPlayersGroups:
            playersGroup.pauseAllAudioPlayers()
        self.playButton.hide()
        self.pausedButton.show()
        startAudioPosition = math.floor((self.audioTimeSlider.value() / self.audioTimeSlider.maximum()) * self.audioDuration)
        if self.audioTimeSlider.value() == self.audioTimeSlider.maximum():
            startAudioPosition = self.audioDuration
        self.currentAudioTime = startAudioPosition
        self.mediaPlayer.set_time(self.currentAudioTime)
        self.mediaPlayer.play()
        audioVolume = math.floor((self.volumeSlider.value() / self.volumeSlider.maximum()) * 100)
        if self.volumeSlider.value() == self.volumeSlider.maximum():
            audioVolume = 100
        self.mediaPlayer.audio_set_volume(audioVolume)
        self._unblockAllSignals()

    def onPauseButtonClicked(self):
        if self.DEBUG_MODE:
            print("Pause button clicked")
        self._blockAllSignals()
        self.pausedButton.hide()
        self.playButton.show()
        self.mediaPlayer.set_pause(1)
        self.updateAudioTimers()
        self._unblockAllSignals()

    def updateAudioTimers(self):
        if self.DEBUG_MODE:
            print("Updating audio timers")
        self._blockAllSignals()
        mediaPosition = self.currentAudioTime
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
        if self.mediaPlayer.get_media() is None:
            return
        updatedPosition = math.floor((changedValue / self.audioTimeSlider.maximum()) * self.audioDuration)
        if changedValue == self.audioTimeSlider.maximum():
            updatedPosition = self.audioDuration
        self.currentAudioTime = updatedPosition
        self.mediaPlayer.set_time(updatedPosition)
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
        self.mediaPlayer.audio_set_volume(updateVolume)
        self._unblockAllSignals()

    def setAudioForPlayer(self, audioFile, audioLength, autoplay):
        if self.DEBUG_MODE:
            print("Set audio for player")
        self._blockAllSignals()
        self.audioDuration = math.floor(audioLength * 1000)
        self.mediaPlayer.stop()
        self.audioMedia = self._vlcInstance.media_new(audioFile)
        self.mediaPlayer.set_media(self.audioMedia)
        self.playButton.setDisabled(False)
        self.pausedButton.setDisabled(False)
        self.pausedButton.hide()
        self.audioTimeSlider.setDisabled(False)
        audioVolume = math.floor((self.volumeSlider.value() / self.volumeSlider.maximum()) * 100)
        if self.volumeSlider.value() == self.volumeSlider.maximum():
            audioVolume = 100
        self.audioTimer.setCurrentAndTotalTimes(0, self.audioDuration // 1000)
        self.updateAudioTimers()
        self.mediaPlayer.audio_set_volume(audioVolume)
        self.mediaPlayer.set_time(0)
        settingsPanel = EntryPoints.MAIN_WINDOW.outputModeSettingsPanel
        if settingsPanel.getStartAheadIsTurnedOn():
            self.currentAudioTime = min(10_000, self.audioDuration // 3)
            self.updateAudioTimers()
        if settingsPanel.getAutoPlayIsTurnedOn() and autoplay:
            self.playButton.hide()
            self.pausedButton.show()
            self.mediaPlayer.play()
            self.mediaPlayer.set_time(self.currentAudioTime)
            audioVolume = math.floor((self.volumeSlider.value() / self.volumeSlider.maximum()) * 100)
            if self.volumeSlider.value() == self.volumeSlider.maximum():
                audioVolume = 100
            self.mediaPlayer.audio_set_volume(audioVolume)
        self._unblockAllSignals()

    def clearAudioFromPlayer(self):
        if self.DEBUG_MODE:
            print("Cleared audio from player")
        self._blockAllSignals()
        self.mediaPlayer.stop()
        if self.mediaPlayer.get_media() is not None:
            self.mediaPlayer.get_media().release()
        self.audioDuration = 0
        self.currentAudioTime = 0
        self.audioMedia = None
        self.playButton.setDisabled(True)
        self.playButton.show()
        self.pausedButton.setDisabled(True)
        self.pausedButton.hide()
        self.audioTimeSlider.setDisabled(True)
        self.audioTimeSlider.setValue(0)
        self.audioTimer.setNoAudioState()
        self._unblockAllSignals()

    def _blockAllSignals(self):
        self.audioTimeSlider.blockSignals(True)

    def _unblockAllSignals(self):
        self.audioTimeSlider.blockSignals(False)
