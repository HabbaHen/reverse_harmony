from PyQt5.QtCore import QThreadPool
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from src.desktop_application.MainWindow import MainWindow
import resources
from src.desktop_application.file_upload.FileUpload import FileUpload

app = QApplication([])
app.setApplicationName("Harmony Reverse Tool")
app.setWindowIcon(QIcon(":/resources/harmony_reverse_tool_icon.png"))
app.setStyle('Fusion')
mainWindow = MainWindow()
mainWindow.show()
FileUpload.APP = app  # needed for fix for `app icon missing after file dialog is opened` issue
QThreadPool.globalInstance().setMaxThreadCount(4)
app.exec()
