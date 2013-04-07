#! /bin/sh

set -x

rm -rf orig
rm -rf copy

mkdir orig
mkdir copy

mkdir orig/somedir

(
  cd orig
  ../../../../dumpdir > ../dump
) || {
  echo "dumpdir fail"
  exit 1
}

(
  cd copy
  ../../../../reversedumpdir ../dump
) || {
  echo "reversedumpdir fail"
  exit 1
}

diff -r orig copy
