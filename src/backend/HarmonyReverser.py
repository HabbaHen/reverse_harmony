import sys
import traceback

from pretty_midi import pretty_midi

from src.backend.ErrorHandle import ErrorHandle


class HarmonyReverser:

    @staticmethod
    def _fileIsMIDI(filename):
        return filename.endswith(".mid")

    def __init__(self, filename):
        self.errorMessage = None
        if not self._fileIsMIDI(filename):
            self.errorMessage = "Only MIDI files supported"
            return
        self.midiFile = self._readMidiFile(filename)

    def getErrorMessage(self):
        return self.errorMessage

    """ Uses default strategy for musical instruments volumes """
    def reverseHarmony(self):
        # self.midiFile - contains midi file
        pass # todo

    def _readMidiFile(self, filename):
        try:
            return pretty_midi.PrettyMIDI(filename)
        except (ValueError, OSError, EOFError):
            print("Tried to read MIDI file, but it's probably not MIDI file", file=sys.stderr)
            with open(ErrorHandle.TRACEBACK_FILE, 'rt') as tracebackFile:
                traceback.print_stack(file=tracebackFile)
            self.errorMessage = "Failed to read file"
            return None
