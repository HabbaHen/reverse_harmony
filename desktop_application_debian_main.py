import os
from desktop_application_main import runDesktopApp


if __name__ == '__main__':
    os.environ["VLC_PLUGIN_PATH"] = "/usr/lib/x86_64-linux-gnu/vlc/plugins"  # fix for VLC
    runDesktopApp()
