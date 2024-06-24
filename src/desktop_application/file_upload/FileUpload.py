from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog
import resources
from src.desktop_application.EntryPoints import EntryPoints


class FileUpload:

    UPLOAD_FILTER = "MIDI Files (*.mid)"
    APP = None

    @staticmethod
    def uploadInputFile(caption):
        filename, fileFilter = QFileDialog.getOpenFileName(caption=caption,
                                                           filter="All Files (*);;MIDI Files (*.mid)",
                                                           initialFilter=FileUpload.UPLOAD_FILTER)
        FileUpload.UPLOAD_FILTER = fileFilter
        FileUpload._fixAppIcon()
        return filename

    @staticmethod
    def chooseOutputFile(caption):
        inputFilename = EntryPoints.MAIN_WINDOW.getCurrentlyChosenFilename()
        if inputFilename:
            if inputFilename.endswith(".mid"):
                inputFilename = inputFilename[:-4] + "-reversed.mp3"
            filename, _ = QFileDialog.getSaveFileName(caption=caption, directory=inputFilename,
                                                      filter="All Files (*)", initialFilter="All Files (*)")
        else:
            filename, _ = QFileDialog.getSaveFileName(caption=caption, filter="All Files (*)",
                                                      initialFilter="All Files (*)")
        FileUpload._fixAppIcon()
        return filename

    @staticmethod
    def _fixAppIcon():
        if FileUpload.APP is not None:
            FileUpload.APP.setWindowIcon(QIcon(":/resources/harmony_reverse_tool_icon.png"))

    def __init__(self):
        raise RuntimeError("FileUpload class is not instantiable")
