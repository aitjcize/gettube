#!/bin/bash

echo 'Version: '
read ver

./chver.sh $ver
cd ../../
cp -r gettube gettube-$ver
mv gettube-$ver gettube/dev
cd gettube/dev/
tar -zcf gettube_$ver.orig.tar.gz gettube-$ver

cd gettube-$ver
dh_make -s -b -p gettube

echo `pwd`
cp dev/rules dev/control debian
cd debian
rm *.ex *.EX README.*
dch -e
cd ..

if [ "$1" == "build" ]; then
  dpkg-buildpackage -rfakeroot
elif [ "$1" == "ppa" ]; then
  debuild -S
fi
