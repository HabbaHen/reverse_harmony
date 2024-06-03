<h1> Current plan </h1>

Rewrite the application in python.

For Windows/Mac/Linux use PyQt for desktop GUI.

For Android/IoS use Kivi for mobile GUI.

For Windows, use NSIS for creating Windows Installer of the application, which includes a script for installing fluidsynth and ffmpeg (see https://stackoverflow.com/questions/74651215/couldnt-find-ffmpeg-or-avconv-python) on Windows.

For Linux and macOs, create a build bash script

For other desktop OS, describe in README.md how to build the app manually (install fluidsynth and ffmpeg, then run python app using requirements.txt)
