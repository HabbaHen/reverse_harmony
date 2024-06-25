import os
from os import path

from midi2audio import FluidSynth
from pretty_midi import pretty_midi
from pydub import AudioSegment
from paths import Paths
from src.backend.ErrorHandle import ErrorHandle


class HarmonyReverser:

    DEFAULT_SOUND_FONT = path.join(Paths.APP_DIRECTORY, "default.sf2")
    TEMPORARY_DIRECTORY = path.join(Paths.APP_DIRECTORY, "temp")
    TEMPORARY_CONVERSION_FILE = path.join(Paths.APP_DIRECTORY, "temp/temp")
    TEMPORARY_ORIGINAL_AUDIO_MP3_FILE = path.join(Paths.APP_DIRECTORY, "temp/original_temp")
    TEMPORARY_REVERSED_AUDIO_MP3_FILE = path.join(Paths.APP_DIRECTORY, "temp/reversed_temp")
    TEMPORARY_REVERSED_MIDI_FILE = path.join(Paths.APP_DIRECTORY, "temp/reversed_midi_temp")

    @staticmethod
    def _fileIsMIDI(filename):
        return filename.endswith(".mid")

    def __init__(self, filename):
        if not path.isdir(self.TEMPORARY_DIRECTORY):
            os.makedirs(self.TEMPORARY_DIRECTORY)
        self._errorMessage = None
        if not self._fileIsMIDI(filename):
            self._errorMessage = "Only MIDI files supported (.mid)"
            return
        self._midiFileName = filename
        self._midiData = self._readMidiFile(filename)

    def getErrorMessage(self):
        return self._errorMessage

    def getOriginalAudioInMp3Format(self):
        if not self._convertMidiToMp3(self._midiFileName, self.TEMPORARY_ORIGINAL_AUDIO_MP3_FILE,
                                      "Original MIDI failed conversion to MP3"):
            return None
        return self.TEMPORARY_ORIGINAL_AUDIO_MP3_FILE

    """ Uses default strategy for musical instruments volumes """
    def getReversedAudioInMp3Format(self):
        try:
            self._reverseMidi(self.TEMPORARY_REVERSED_MIDI_FILE, 16)
        except Exception as error:
            ErrorHandle.handleError(error, f"Failed to reverse MIDI `{self._midiFileName}`")
            self._errorMessage = "Failed to reverse MIDI"
            return None
        if not self._convertMidiToMp3(self.TEMPORARY_REVERSED_MIDI_FILE, self.TEMPORARY_REVERSED_AUDIO_MP3_FILE,
                                      "Reversed MIDI failed conversion to MP3"):
            return None
        return self.TEMPORARY_REVERSED_AUDIO_MP3_FILE

    def _reverseMidi(self, reversedMidiFileName, halfTonesShift):
        notes_by_instruments = dict()
        instrument_number = 0
        instrument_types = dict()
        minV = 127
        maxV = 0
        for instrument in self._midiData.instruments:
            instrument_types[instrument_number] = instrument.program
            partiture = []
            for note in instrument.notes:
                partiture.append([note.pitch, note.start, note.end, note.velocity])
                if maxV < note.pitch:
                    maxV = note.pitch
                if minV > note.pitch:
                    minV = note.pitch
            notes_by_instruments[instrument_number] = partiture
            instrument_number += 1
        reversed_midi = pretty_midi.PrettyMIDI()
        for instrument_number in instrument_types:
            partiture = pretty_midi.Instrument(program=instrument_types[instrument_number])
            for row in notes_by_instruments[instrument_number]:
                note = pretty_midi.Note(
                    velocity=int(row[3]),
                    pitch=int(maxV + minV + halfTonesShift - row[0]),
                    start=float(row[1]),
                    end=float(row[2]))
                partiture.notes.append(note)
            reversed_midi.instruments.append(partiture)
        reversed_midi.write(reversedMidiFileName)

    def _convertMidiToMp3(self, midiFileName, mp3FileName, errorMessage):
        try:
            fs = FluidSynth(self.DEFAULT_SOUND_FONT)
            fs.midi_to_audio(midiFileName, self.TEMPORARY_CONVERSION_FILE)
            AudioSegment.from_wav(self.TEMPORARY_CONVERSION_FILE).export(mp3FileName, format="mp3")
            return True
        except Exception as error:
            ErrorHandle.handleError(error, f"Conversion from MIDI to MP3 failed with error: `{errorMessage}`")
            self._errorMessage = errorMessage
            return False

    def _readMidiFile(self, filename):
        try:
            return pretty_midi.PrettyMIDI(filename)
        except Exception as error:
            ErrorHandle.handleError(error, "Tried to read MIDI file, but it's probably not MIDI file")
            self._errorMessage = "Failed to open or process MIDI file"
            return None
