#!/bin/bash
echo '<!DOCTYPE RCC><RCC version="1.0">' > resources.qrc
if [ $? -ne 0 ]; then
  exit 1
fi
echo '<qresource>' >> resources.qrc
if [ $? -ne 0 ]; then
  exit 1
fi
for filename in resources/*; do
  echo '<file>'"${filename}"'</file>' >> resources.qrc
  if [ $? -ne 0 ]; then
    exit 1
  fi
done
echo '</qresource>' >> resources.qrc
if [ $? -ne 0 ]; then
  exit 1
fi
echo '</RCC>' >> resources.qrc
if [ $? -ne 0 ]; then
  exit 1
fi
pyrcc5 -o resources.py resources.qrc
if [ $? -ne 0 ]; then
  exit 1
fi
exit 0