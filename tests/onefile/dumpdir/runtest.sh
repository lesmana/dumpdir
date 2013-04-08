#! /bin/sh

set -x

expected="\
f somefile
"

arrange() {
  rm -rf workdir
  mkdir workdir
  touch workdir/somefile

  echo -n "$expected" > expected
}

act() {
  (
    cd workdir
    ../../../../dumpdir > ../actual
  )
}

assert() {
  diff actual expected
}

runtest() {
  arrange
  act
  assert
}

runtest
