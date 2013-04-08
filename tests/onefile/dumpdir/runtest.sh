#! /bin/sh

set -x

rm -rf workdir
mkdir workdir
touch workdir/somefile

expected="\
f somefile
"

echo -n "$expected" > expected

(
  cd workdir
  ../../../../dumpdir > ../actual
)

diff actual expected
