from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from src.desktop_application.MainWindow import MainWindow
import resources
from src.desktop_application.file_upload.FileUpload import FileUpload

app = QApplication([])
app.setApplicationName("Harmony Reverse Tool")
app.setWindowIcon(QIcon(":/resources/icons/harmony_reverse_tool_icon.png"))
app.setStyle('Fusion')
mainWindow = MainWindow()
mainWindow.show()
FileUpload.APP = app  # fix for `app icon missing after file dialog is opened` issue
app.exec()
