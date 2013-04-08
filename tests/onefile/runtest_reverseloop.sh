#! /bin/sh

set -x

orig="\
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

  echo -n "$orig" > orig
}

act() {
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
}

assert() {
  diff -r orig copy
}

runtest() {
  arrange
  act
  assert
}

setuptestenvironment
runtest
