#! /bin/sh

set -x

expected="\
f somefile
"

rm -rf workdir
mkdir workdir
touch workdir/somefile

echo -n "$expected" > expected

(
  cd workdir
  ../../../../dumpdir > ../actual
)

diff actual expected
