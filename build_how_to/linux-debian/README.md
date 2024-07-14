<h2> IMPORTANT NOTES </h2>

For development, `Jetbrains PyCharm` was used. It is better to use it for building packages/installers, because it creates virtual environment for you, so you don't need to handle some issues with having some libraries/packages already installed on your system with different versions.

`Python3.10` should be used for building packages/installers of the project across all OS 

<h2> Building .deb package for Linux using script </h2>

You need to have `pyrcc5`, `pyinstaller` and `dpkg-deb` installed:

```
sudo apt install pyqt5-dev-tools dpkg
pip install -r requirements.txt
```

Run script for building .deb package:

```
./build_debian_package.sh <current-version> <architecture>
```

For example,

```
./build_debian_package.sh 1.0-1 amd64
```

<h2> Building .deb package for Linux manually </h2>

You need to have `pyrcc5`, `pyinstaller` and `dpkg-deb` installed:

```
sudo apt install pyqt5-dev-tools=5.15.6 pyinstaller=6.8.0 dpkg
pip install -r requirements.txt
```

Building PyQt resources (icons and such):

```
./compile_resources.sh
```

Building PyQt into single executable using PyInstaller:

```
pyinstaller harmony-reverser.spec
```

OR

```
pyinstaller --name="harmony-reverser" --onefile --windowed --add-data="default.sf2:." desktop_application_main.py
```

Remove unnecessary directory created by PyInstaller:

```
rm -rf ./build
```

Now, executable should have path `dist/harmony-reverser`, we need to put it into `harmony-reverser-{architecture}_{current-version}/usr/local/bin` directory:

For this, we need to setup version of debian package first, which is located at `DEBIAN/control` in line `Version: {current-version}`

```
DEBIAN_DESKTOP_APPLICATION_VERSION="{put-new-version-here}"
sed -i 's/^Version: \(.*\)$/Version: '"${DEBIAN_DESKTOP_APPLICATION_VERSION}"'/' DEBIAN/control
```

Also we need to set architecture for our package:

```
DEBIAN_DESKTOP_APPLICATION_ARCHITECTURE="{put-architecture-here, e.g. i386}"
sed -i 's/^Architecture: \(.*\)$/Architecture: '"${DEBIAN_DESKTOP_APPLICATION_ARCHITECTURE}"'/' DEBIAN/control
```

Now, we need to create our package directory and copy `DEBIAN` directory into it

```
DEBIAN_PACKAGE_DIRECTORY="harmony-reverser-${DEBIAN_DESKTOP_APPLICATION_ARCHITECTURE}_${DEBIAN_DESKTOP_APPLICATION_VERSION}"
if [ -d "${DEBIAN_PACKAGE_DIRECTORY}" ]; then
  rm -rf "${DEBIAN_PACKAGE_DIRECTORY}"
fi
mkdir "${DEBIAN_PACKAGE_DIRECTORY}"
cp -r ./DEBIAN "${DEBIAN_PACKAGE_DIRECTORY}/DEBIAN"
```

And then to move executable of our application into `${DEBIAN_PACKAGE_DIRECTORY}/usr/local/bin`

```
mkdir -p "${DEBIAN_PACKAGE_DIRECTORY}/usr/local/bin"
mv ./dist/harmony-reverser "${DEBIAN_PACKAGE_DIRECTORY}/usr/local/bin"
```

Cleanup `dist` directory created by PyInstaller

```
rm -r dist
```

And, finally, build `.deb` package using `dpkg-deb`

```
dpkg-deb --build "${DEBIAN_PACKAGE_DIRECTORY}"
```

The Debian package is now in root folder as `${DEBIAN_PACKAGE_DIRECTORY}.deb` file, so we can cleanup package directory:

```
rm -rf ./"${DEBIAN_PACKAGE_DIRECTORY}"
```
