#! /bin/sh

set -x

expected="\
f somefile
"

setuptestenvironment() {
  testenvironment="$0_environment"
  rm -rf "$testenvironment"
  mkdir "$testenvironment"
  cd "$testenvironment"
}

arrange() {
  rm -rf workdir
  mkdir workdir
  touch workdir/somefile

  echo -n "$expected" > expected
}

act() {
  (
    cd workdir
    ../../../../../dumpdir > ../actual
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

setuptestenvironment
runtest
