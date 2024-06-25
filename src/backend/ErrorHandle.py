import os
import sys
import traceback

from paths import Paths


class ErrorHandle:

    TRACEBACK_FILE = os.path.join(Paths.APP_DIRECTORY, "error_traceback.txt")

    @staticmethod
    def handleError(error, tracebackErrorMessage):
        print(tracebackErrorMessage, file=sys.stderr)
        with open(ErrorHandle.TRACEBACK_FILE, 'wt') as tracebackFile:
            traceback.print_exception(error, file=tracebackFile)
            tracebackFile.write("\n")
            tracebackFile.write(tracebackErrorMessage)

    def __init__(self):
        raise RuntimeError("ErrorHandle is not instantiable")
