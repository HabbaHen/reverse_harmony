
class AudioTimer:

    def __init__(self, currentTimeLabel, totalTimeLabel):
        super().__init__()
        self.currentTimeLabel = currentTimeLabel
        self.totalTimeLabel = totalTimeLabel
        self._audioIsSet = False
        self.setNoAudioState()

    def setCurrentAndTotalTimes(self, currentSeconds, totalSeconds):
        currentMinutes = str(currentSeconds // 60)
        currentSeconds = str(currentSeconds % 60)
        if len(currentSeconds) == 1:
            currentSeconds = "0" + currentSeconds
        totalMinutes = str(totalSeconds // 60)
        totalSeconds = str(totalSeconds % 60)
        if len(totalSeconds) == 1:
            totalSeconds = "0" + totalSeconds
        self.currentTimeLabel.setText(currentMinutes + ":" + currentSeconds)
        self.totalTimeLabel.setText(totalMinutes + ":" + totalSeconds)
        self._audioIsSet = True

    def setCurrentTime(self, currentSeconds):
        currentMinutes = str(currentSeconds // 60)
        currentSeconds = str(currentSeconds % 60)
        if len(currentSeconds) == 1:
            currentSeconds = "0" + currentSeconds
        self.currentTimeLabel.setText(currentMinutes + ":" + currentSeconds)

    def setNoAudioState(self):
        self.currentTimeLabel.setText("0:00")
        self.totalTimeLabel.setText("0:00")
        self._audioIsSet = False
