import os

from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from src.backend.HarmonyReverser import HarmonyReverser
from src.desktop_application.MainWindow import MainWindow
import resources
from src.desktop_application.file_upload.FileUpload import FileUpload


def cleanUp():
    if os.path.exists(HarmonyReverser.TEMPORARY_CONVERSION_FILE):
        os.remove(HarmonyReverser.TEMPORARY_CONVERSION_FILE)
    if os.path.exists(HarmonyReverser.TEMPORARY_ORIGINAL_AUDIO_MP3_FILE):
        os.remove(HarmonyReverser.TEMPORARY_ORIGINAL_AUDIO_MP3_FILE)
    if os.path.exists(HarmonyReverser.TEMPORARY_REVERSED_AUDIO_MP3_FILE):
        os.remove(HarmonyReverser.TEMPORARY_REVERSED_AUDIO_MP3_FILE)
    if os.path.exists(HarmonyReverser.TEMPORARY_REVERSED_MIDI_FILE):
        os.remove(HarmonyReverser.TEMPORARY_REVERSED_MIDI_FILE)


cleanUp()
app = QApplication([])
app.setApplicationName("Harmony Reverse Tool")
app.setWindowIcon(QIcon(":/resources/harmony_reverse_tool_icon.png"))
app.setStyle('Fusion')
app.aboutToQuit.connect(cleanUp)
mainWindow = MainWindow()
mainWindow.show()
FileUpload.APP = app  # needed for fix for `app icon missing after file dialog is opened` issue
QThreadPool.globalInstance().setMaxThreadCount(4)
app.exec()
