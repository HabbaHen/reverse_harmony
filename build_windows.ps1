pyinstaller .\harmony-reverser-windows.spec
rm -r .\build\
mv .\dist\harmony-reverser.exe .\HarmonyReverser.exe
rm .\dist\