from pretty_midi import pretty_midi
from midi2audio import FluidSynth
from src.backend.ErrorHandle import ErrorHandle


class HarmonyReverser:

    @staticmethod
    def _fileIsMIDI(filename):
        return filename.endswith(".mid")

    def __init__(self, filename):
        self._errorMessage = None
        if not self._fileIsMIDI(filename):
            self._errorMessage = "Only MIDI files supported (.mid)"
            return
        self._midiFile = self._readMidiFile(filename)

    def getErrorMessage(self):
        return self._errorMessage

    def getOriginalAudioInMp3Format(self):
        # self._midiFile - contains midi file
        pass # todo

    """ Uses default strategy for musical instruments volumes """
    def getReversedAudioInMp3Format(self):
        # self._midiFile - contains midi file
        pass # todo

    def _readMidiFile(self, filename):
        try:
            return pretty_midi.PrettyMIDI(filename)
        except Exception as error:
            ErrorHandle.handleError(error, "Tried to read MIDI file, but it's probably not MIDI file")
            self._errorMessage = "Failed to open or process MIDI file"
            return None
