from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QButtonGroup, QRadioButton, QCheckBox)


class OutputModeSettingsPanel(QWidget):

    AUDIO_PREVIEW_MODE = "Audio Preview"
    SAVE_AS_MIDI_MODE = "Save Audio as .mp3"
    AUTO_PLAY_CHECKBOX = "Auto-Play Audio"
    START_AHEAD_CHECKBOX = "Start Ahead (by 10 seconds)"

    def __init__(self):
        super().__init__()
        mainLayout = QHBoxLayout()
        outputModeLayout = QVBoxLayout()
        audioPreviewModeLayout = QVBoxLayout()
        # Radio buttons setup
        self.audioPreviewRadioButton = QRadioButton(self.AUDIO_PREVIEW_MODE)
        self.saveAsMidiRadioButton = QRadioButton(self.SAVE_AS_MIDI_MODE)
        outputModeLayout.addWidget(self.audioPreviewRadioButton, stretch=0)
        outputModeLayout.addWidget(self.saveAsMidiRadioButton, stretch=0)
        outputModeLayout.addStretch(stretch=1)
        outputModeRadioButtonGroup = QButtonGroup(self)
        outputModeRadioButtonGroup.addButton(self.audioPreviewRadioButton)
        outputModeRadioButtonGroup.addButton(self.saveAsMidiRadioButton)
        outputModeRadioButtonGroup.setExclusive(True)
        self.audioPreviewRadioButton.setChecked(True)
        self.audioPreviewRadioButton.toggled.connect(self.onToggle)
        self.saveAsMidiRadioButton.toggled.connect(self.onToggle)
        # Audio Preview checkboxes setup
        self.autoPlayAudioCheckbox = QCheckBox(self.AUTO_PLAY_CHECKBOX)
        self.startAheadCheckbox = QCheckBox(self.START_AHEAD_CHECKBOX)
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
        if self.saveAsMidiRadioButton.isChecked():
            return self.SAVE_AS_MIDI_MODE
        return None

    def getAutoPlayIsTurnedOn(self):
        return self.audioPreviewRadioButton.isChecked() and self.autoPlayAudioCheckbox.isChecked()

    def getStartAheadIsTurnedOn(self):
        return self.getAutoPlayIsTurnedOn() and self.startAheadCheckbox.isChecked()

    def onToggle(self):
        if not self.audioPreviewRadioButton.isChecked():
            self.autoPlayAudioCheckbox.hide()
            self.startAheadCheckbox.hide()
            return
        self.autoPlayAudioCheckbox.show()
        if self.autoPlayAudioCheckbox.isChecked():
            self.startAheadCheckbox.show()
        else:
            self.startAheadCheckbox.hide()
