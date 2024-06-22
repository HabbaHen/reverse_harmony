import os


class ErrorHandle:

    APP_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    TRACEBACK_FILE = os.path.join(APP_DIRECTORY, "error_traceback.txt")
