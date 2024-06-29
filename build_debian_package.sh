#!/bin/bash
if [ $# -ne 2 ]; then
  echo "Incorrect number of parameters provided."
  echo "Usage: $0 <current-version> <architecture>"
  echo "For example: $0 1.0-1 i386"
  exit 1
fi
DEBIAN_DESKTOP_APPLICATION_VERSION="$1"
DEBIAN_DESKTOP_APPLICATION_ARCHITECTURE="$2"
./compile_resources.sh
if [ $? -ne 0 ]; then
  echo "Failed to compile resources (images and etc)"
  exit 1
fi
pyinstaller harmony-reverser.spec
if [ $? -ne 0 ]; then
  echo "Failed to compile project using pyinstaller"
  exit 1
fi
rm -rf ./build
if [ $? -ne 0 ]; then
  echo "Failed to remove unnecessary directory build"
  rm -rf ./dist
  exit 1
fi
sed -i 's/^Version: \(.*\)$/Version: '"${DEBIAN_DESKTOP_APPLICATION_VERSION}"'/' DEBIAN/control
if [ $? -ne 0 ]; then
  echo "Failed to setup package version in DEBIAN/control"
  rm -rf ./dist
  exit 1
fi
sed -i 's/^Architecture: \(.*\)$/Architecture: '"${DEBIAN_DESKTOP_APPLICATION_ARCHITECTURE}"'/' DEBIAN/control
if [ $? -ne 0 ]; then
  echo "Failed to setup package architecture in DEBIAN/control"
  rm -rf ./dist
  exit 1
fi
APPROXIMATE_APP_SIZE="$(du -ks ./dist/harmony-reverser | cut -f 1)"
if [ $? -ne 0 ]; then
  echo "Failed to compute approximate size of the application"
  rm -rf ./dist
  exit 1
fi
sed -i 's/^Installed-Size: \(.*\)$/Installed-Size: '"${APPROXIMATE_APP_SIZE}"'/' DEBIAN/control
if [ $? -ne 0 ]; then
  echo "Failed to setup package approximate size in DEBIAN/control"
  rm -rf ./dist
  exit 1
fi
DEBIAN_PACKAGE_DIRECTORY="harmony-reverser-${DEBIAN_DESKTOP_APPLICATION_ARCHITECTURE}_${DEBIAN_DESKTOP_APPLICATION_VERSION}"
if [ -d "${DEBIAN_PACKAGE_DIRECTORY}" ]; then
  rm -rf "${DEBIAN_PACKAGE_DIRECTORY}"
  if [ $? -ne 0 ]; then
    echo "Failed to remove unnecessary directory ${DEBIAN_PACKAGE_DIRECTORY}"
    rm -rf ./dist
    exit 1
  fi
fi
mkdir "${DEBIAN_PACKAGE_DIRECTORY}"
if [ $? -ne 0 ]; then
  echo "Failed to create directory ${DEBIAN_PACKAGE_DIRECTORY}"
  rm -rf ./dist
  exit 1
fi
cp -r ./DEBIAN "${DEBIAN_PACKAGE_DIRECTORY}/DEBIAN"
if [ $? -ne 0 ]; then
  echo "Failed to copy contents of DEBIAN directory to ${DEBIAN_PACKAGE_DIRECTORY}/DEBIAN"
  rm -rf ./dist
  rm -rf ./"${DEBIAN_PACKAGE_DIRECTORY}"
  exit 1
fi
mkdir -p "${DEBIAN_PACKAGE_DIRECTORY}/usr/local/bin"
if [ $? -ne 0 ]; then
  echo "Failed to create directory ${DEBIAN_PACKAGE_DIRECTORY}/usr/local/bin"
  rm -rf ./dist
  rm -rf ./"${DEBIAN_PACKAGE_DIRECTORY}"
  exit 1
fi
mv ./dist/harmony-reverser "${DEBIAN_PACKAGE_DIRECTORY}/usr/local/bin"
if [ $? -ne 0 ]; then
  echo "Failed to move application executable into ${DEBIAN_PACKAGE_DIRECTORY}/usr/local/bin"
  rm -rf ./dist
  rm -rf ./"${DEBIAN_PACKAGE_DIRECTORY}"
  exit 1
fi
rm -r ./dist
if [ $? -ne 0 ]; then
  echo "Failed to remove directory dist"
  rm -rf ./"${DEBIAN_PACKAGE_DIRECTORY}"
  exit 1
fi
dpkg-deb --build "${DEBIAN_PACKAGE_DIRECTORY}"
if [ $? -ne 0 ]; then
  echo "Failed to build .deb package"
  rm -rf ./"${DEBIAN_PACKAGE_DIRECTORY}"
  exit 1
fi
rm -rf ./"${DEBIAN_PACKAGE_DIRECTORY}"
if [ $? -ne 0 ]; then
  echo "Failed to remove directory ${DEBIAN_PACKAGE_DIRECTORY} which was used for building .deb package"
  exit 1
fi
exit 0
