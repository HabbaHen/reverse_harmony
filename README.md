<h1> Current plan </h1>

- Current bugs:
  - Fix bug on Windows with audio slider going to 0 seconds on first play button press (even if it was scrolled)
  - Fix bug on Windows with audio slider and audio player not being synched properly
- For Windows, use NSIS for creating Windows Installer of the application, which includes a script for installing fluidsynth and ffmpeg (see https://stackoverflow.com/questions/74651215/couldnt-find-ffmpeg-or-avconv-python) on Windows.
  - Describe in `build-how-to` the process of building Windows installer
- For MacOs, create a package using `Packages` application
- Linux (Debian) - packaging process is done and described


<h2> Installing the application </h2>

Check [Releases](https://github.com/HabbaHen/reverse_harmony/releases) of this project

<h2>Running desktop application using source code</h2>

Install ffmpeg (>= 4.4.2), fluidsynth (>= 2.2.5), python (>= 3.10) and pip on your system, then in root directory run:

```
pip install -r requirements.txt
python3 desktop_application_main.py
```

<h2> Manuals for building application installers for different operating systems </h2>

Manuals are located [here](https://github.com/HabbaHen/reverse_harmony/tree/main/build_how_to)
