#! /bin/sh

set -x

rm -rf actual
rm -rf expected

inputfile="\
f somefile
"

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
