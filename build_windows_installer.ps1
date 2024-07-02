pyinstaller .\harmony-reverser-windows.spec
if ( -not $? ) {
    'Failed to compile project using pyinstaller'
    exit 1
}
rm -r .\build\
if ( -not $? ) {
    'Failed to remove directory `build`'
    rm -r .\dist\
    exit 1
}
mv .\dist\harmony-reverser.exe .\HarmonyReverser.exe
if ( -not $? ) {
    'Failed to move application executable file'
    exit 1
}
rm .\dist\
if ( -not $? ) {
    'Failed to remove directory `dist`'
    exit 1
}

exit 0