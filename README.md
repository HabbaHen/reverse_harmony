<h1> Current plan </h1>

Rewrite the application in python.

For Windows/Mac/Linux use PyQt for desktop GUI.

For Android/IoS use Kivi for mobile GUI.

For Windows, use NSIS for creating Windows Installer of the application, which includes a script for installing fluidsynth and ffmpeg (see https://stackoverflow.com/questions/74651215/couldnt-find-ffmpeg-or-avconv-python) on Windows.

For Linux and macOs, create a build bash script OR better create .deb for Debian/Ubuntu and .dmg for macOS 

For other desktop OS, describe in README.md how to build the app manually (install fluidsynth and ffmpeg, then run python app using requirements.txt)


<h2> Installing the application </h2>

Check `Releases` of this project on GitHub

<h2> Manuals for building application installers for different operating systems </h2>

Manuals are located [here](https://github.com/HabbaHen/reverse_harmony/tree/main/build_how_to)

<h2>Running desktop application using source code</h2>

Install ffmpeg (>= 4.4.2), fluidsynth (>= 2.2.5), python (>= 3.10) and pip on your system, then in root directory run:

```
pip install -r requirements.txt
python3 desktop_application_main.py
```
