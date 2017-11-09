#! /bin/sh

PATH="$PWD:$PATH"

cd tests
rm -rf actualtests
mkdir -p actualtests
cp -a templates/* actualtests
cd actualtests
shut -r
