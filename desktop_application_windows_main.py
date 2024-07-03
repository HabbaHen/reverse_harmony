from desktop_application_main import runDesktopApp
import subprocess


# Creates wrapper for subprocess.Popen to not create process window on Windows
def wrapSubprocessPopen():
    _originalOpen = subprocess.Popen
    def _newOpen(*args, **kwargs):
        if 'creationflags' not in kwargs:
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
        return _originalOpen(*args, **kwargs)
    subprocess.Popen = _newOpen

if __name__ == '__main__':
    wrapSubprocessPopen()
    runDesktopApp()
