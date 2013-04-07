#! /bin/sh

set -x

rm -rf workdir
mkdir workdir

(
  cd workdir
  touch somefile
  ../../../../dumpdir > ../actual
)

expected="\
f somefile
"

echo -n "$expected" > expected

diff actual expected
