import os
import sys
import traceback


class ErrorHandle:

    APP_DIRECTORY = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    TRACEBACK_FILE = os.path.join(APP_DIRECTORY, "error_traceback.txt")

    @staticmethod
    def handleError(error, tracebackErrorMessage):
        print(tracebackErrorMessage, file=sys.stderr)
        with open(ErrorHandle.TRACEBACK_FILE, 'wt') as tracebackFile:
            traceback.print_exception(error, file=tracebackFile)
            tracebackFile.write("\n")
            tracebackFile.write(tracebackErrorMessage)

    def __init__(self):
        raise RuntimeError("ErrorHandle is not instantiable")
