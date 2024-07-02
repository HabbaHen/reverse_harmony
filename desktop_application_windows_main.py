from desktop_application_main import runDesktopApp
import subprocess
import os


# Creates wrapper for subprocess.Popen to not create process window on Windows
def wrapSubprocessPopen():
    _originalOpen = subprocess.Popen
    def _newOpen(*args, **kwargs):
        if 'creationflags' not in kwargs:
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
        return _originalOpen(*args, **kwargs)
    subprocess.Popen = _newOpen

# PyQt QMediaPlayer goes nuts without this, this was also discussed at
# https://forum.pythonguis.com/t/is-it-just-me-or-is-qmediaplayer-not-working-properly/401
def fixPyQtMediaPlayer():
    os.environ['QT_MULTIMEDIA_PREFERRED_PLUGINS'] = 'windowsmediafoundation'

if __name__ == '__main__':
    wrapSubprocessPopen()
    fixPyQtMediaPlayer()
    runDesktopApp()
