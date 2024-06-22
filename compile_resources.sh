#!/bin/bash
echo '<!DOCTYPE RCC><RCC version="1.0">' > resources.qrc
echo '<qresource>' >> resources.qrc
for filename in resources/icons/*; do
  echo '<file>'"${filename}"'</file>' >> resources.qrc
done
echo '</qresource>' >> resources.qrc
echo '</RCC>' >> resources.qrc
pyrcc5 -o resources.py resources.qrc