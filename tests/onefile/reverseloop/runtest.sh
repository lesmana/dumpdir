#! /bin/sh

set -x

orig="\
f somefile
"

rm -rf workdir
mkdir workdir

echo -n "$orig" > orig

(
  cd workdir
  ../../../../reversedumpdir ../orig
) || {
  echo "reversedumpdir fail"
  exit 1
}

(
  cd workdir
  ../../../../dumpdir > ../copy
) || {
  echo "dumpdir fail"
  exit 1
}

diff -r orig copy
