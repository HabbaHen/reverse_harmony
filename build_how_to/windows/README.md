<h2> IMPORTANT NOTES </h2>

For development, `Jetbrains PyCharm` was used. It is better to use it for building packages/installers, because it creates virtual environment for you, so you don't need to handle some issues with having some libraries/packages already installed on your system with different versions.

`Python3.10` should be used for building packages/installers of the project across all OS 


<h2> Building NSIS installer for Windows using script </h2>

Before building NSIS installer for Windows, you need to run `compile_resources.sh` script on any system which can run `bash` scripts. Only after the script updates `resources.py` file, you can proceed with building NSIS installer.

Download all required python libraries and `pyinstaller`:

```
pip install -r requirements.txt
pip install pyinstaller==6.8.0
```

Now, just run PowerShell script to build NSIS installer:

```
.\build_windows_installer.ps1
```


<h2> Building NSIS installer for Windows manually </h2>

Before building NSIS installer for Windows, you need to run `compile_resources.sh` script on any system which can run `bash` scripts. Only after the script updates `resources.py` file, you can proceed with building NSIS installer.

Download all required python libraries and `pyinstaller`:

```
pip install -r requirements.txt
pip install pyinstaller==6.8.0
```

Now, generate single executable of desktop application using `pyinstaller`:

```
pyinstaller .\harmony-reverser-windows.spec
```

After that cleanup some data generated by `pyinstaller`: 

```
rm -r .\build\
mv .\dist\harmony-reverser.exe .\HarmonyReverser.exe
rm .\dist\
```