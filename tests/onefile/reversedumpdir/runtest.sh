#! /bin/sh

set -x

inputfile="\
f somefile
"

rm -rf actual
rm -rf expected

echo -n "$inputfile" > inputfile

mkdir expected
touch expected/somefile

mkdir actual

(
  cd actual
  ../../../../reversedumpdir ../inputfile
) || {
  echo "fail"
  exit 1
}

diff -r actual expected
