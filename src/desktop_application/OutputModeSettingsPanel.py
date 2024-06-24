from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup, QRadioButton, QCheckBox)

from src.desktop_application.EntryPoints import EntryPoints


class OutputModeSettingsPanel(QWidget):

    AUDIO_PREVIEW_MODE = "Audio Preview"
    SAVE_AUDIO_AS_MP3_MODE = "Save Audio as .mp3"
    AUTO_PLAY_CHECKBOX = "Auto-Play Audio"
    START_AHEAD_CHECKBOX = "Start Ahead (by 10 seconds)"

    def __init__(self):
        super().__init__()
        mainLayout = QHBoxLayout()
        outputModeLayout = QVBoxLayout()
        audioPreviewModeLayout = QVBoxLayout()
        # Radio buttons setup
        self.audioPreviewRadioButton = QRadioButton(self.AUDIO_PREVIEW_MODE)
        self.audioPreviewRadioButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.saveAudioAsMp3RadioButton = QRadioButton(self.SAVE_AUDIO_AS_MP3_MODE)
        self.saveAudioAsMp3RadioButton.setCursor(QCursor(Qt.PointingHandCursor))
        outputModeLayout.addWidget(self.audioPreviewRadioButton, stretch=0)
        outputModeLayout.addWidget(self.saveAudioAsMp3RadioButton, stretch=0)
        outputModeLayout.addStretch(stretch=1)
        outputModeRadioButtonGroup = QButtonGroup(self)
        outputModeRadioButtonGroup.addButton(self.audioPreviewRadioButton)
        outputModeRadioButtonGroup.addButton(self.saveAudioAsMp3RadioButton)
        outputModeRadioButtonGroup.setExclusive(True)
        self.audioPreviewRadioButton.setChecked(True)
        self.audioPreviewRadioButton.toggled.connect(self.onToggle)
        self.saveAudioAsMp3RadioButton.toggled.connect(self.onToggle)
        # Audio Preview checkboxes setup
        self.autoPlayAudioCheckbox = QCheckBox(self.AUTO_PLAY_CHECKBOX)
        self.autoPlayAudioCheckbox.setCursor(QCursor(Qt.PointingHandCursor))
        self.startAheadCheckbox = QCheckBox(self.START_AHEAD_CHECKBOX)
        self.startAheadCheckbox.setCursor(QCursor(Qt.PointingHandCursor))
        audioPreviewModeLayout.addWidget(self.autoPlayAudioCheckbox, stretch=0)
        audioPreviewModeLayout.addWidget(self.startAheadCheckbox, stretch=0)
        audioPreviewModeLayout.addStretch(stretch=1)
        self.autoPlayAudioCheckbox.toggled.connect(self.onToggle)
        self.startAheadCheckbox.toggled.connect(self.onToggle)
        # Main layout setup
        mainLayout.addLayout(outputModeLayout, stretch=0)
        mainLayout.addSpacing(40)
        mainLayout.addLayout(audioPreviewModeLayout, stretch=0)
        mainLayout.addStretch(stretch=1)
        self.setLayout(mainLayout)
        self.onToggle()

    def getOutputMode(self):
        if self.audioPreviewRadioButton.isChecked():
            return self.AUDIO_PREVIEW_MODE
        if self.saveAudioAsMp3RadioButton.isChecked():
            return self.SAVE_AUDIO_AS_MP3_MODE
        return None

    def getAutoPlayIsTurnedOn(self):
        return self.audioPreviewRadioButton.isChecked() and self.autoPlayAudioCheckbox.isChecked()

    def getStartAheadIsTurnedOn(self):
        return self.getAutoPlayIsTurnedOn() and self.startAheadCheckbox.isChecked()

    def onToggle(self):
        EntryPoints.MAIN_WINDOW.onOutputModeSettingsPanelToggle(self)
        if not self.audioPreviewRadioButton.isChecked():
            self.autoPlayAudioCheckbox.hide()
            self.startAheadCheckbox.hide()
            return
        self.autoPlayAudioCheckbox.show()
        if self.autoPlayAudioCheckbox.isChecked():
            self.startAheadCheckbox.show()
        else:
            self.startAheadCheckbox.hide()
