from os import path

from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout)

from src.desktop_application.CentralWidget import CentralWidget
from src.desktop_application.EntryPoints import EntryPoints
from src.desktop_application.OutputModeSettingsPanel import OutputModeSettingsPanel
from src.desktop_application.SaveFileButton import SaveFileButton
from src.desktop_application.file_picker.InputFilePicker import InputFilePicker


class MainWindow(QMainWindow):

    def __init__(self):
        EntryPoints.MAIN_WINDOW = self
        super().__init__()
        self.inputFilePicker = InputFilePicker(70, 70)
        self.saveFileAsMp3Stripe = SaveFileButton(100, 100)
        self.saveFileAsMp3Stripe.hide()
        layout = QVBoxLayout()
        layout.addWidget(self.inputFilePicker, stretch=0)
        layout.addWidget(OutputModeSettingsPanel(), stretch=0)
        layout.addStretch(stretch=1)
        layout.addWidget(self.saveFileAsMp3Stripe, stretch=0)
        self.saveFileAsMp3Stripe.initializeState()
        centralWidget = CentralWidget(self)
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)
        self.resize(640, 400)

    def getCurrentlyChosenFilename(self):
        return self.inputFilePicker.chosenFileLabel.toolTip()

    def showErrorMessage(self, errorMessage):
        self.inputFilePicker.errorMessageLabel.setText(errorMessage)
        self.inputFilePicker.errorMessageLabel.show()

    """ Return True if file is fine, False otherwise. """
    def handleBigSizeInputFileUpload(self, filename):
        try:
            if path.getsize(filename) > 500 * 1024 * 1024:
                EntryPoints.MAIN_WINDOW.showErrorMessage("File size is too big (> 500 MB)")
                return False
        except OSError:
            return False
        return True

    def handleAudioSetup(self, originalAudio, reversedAudio):
        self.saveFileAsMp3Stripe.setEnabledState()
        pass # todo

    def onOutputModeSettingsPanelToggle(self, settingsPanel):
        if not(settingsPanel.saveAudioAsMp3RadioButton.isChecked()) and self.saveFileAsMp3Stripe.isVisible():
            self.onSaveAudioAsMp3ModeSwitchedFrom()
        if settingsPanel.saveAudioAsMp3RadioButton.isChecked() and self.saveFileAsMp3Stripe.isHidden():
            self.onSaveAudioAsMp3ModeSwitchedTo()
            return
        pass # todo

    def onAudioPreviewModeSwitchedFrom(self):
        pass # todo

    def onAudioPreviewModeSwitchedTo(self):
        pass # todo

    def onSaveAudioAsMp3ModeSwitchedFrom(self):
        self.saveFileAsMp3Stripe.hideFeedbackMessage()
        self.saveFileAsMp3Stripe.hide()

    def onSaveAudioAsMp3ModeSwitchedTo(self):
        self.saveFileAsMp3Stripe.show()
