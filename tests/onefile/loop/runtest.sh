#! /bin/sh

set -x

setuptestenvironment() {
  testenvironment="$0_environment"
  rm -rf "$testenvironment"
  mkdir "$testenvironment"
  cd "$testenvironment"
}

arrange() {
  rm -rf orig
  rm -rf copy

  mkdir orig
  mkdir copy

  touch orig/somefile
}

act() {
  (
    cd orig
    ../../../../../dumpdir > ../dump
  ) || {
    echo "dumpdir fail"
    exit 1
  }

  (
    cd copy
    ../../../../../reversedumpdir ../dump
  ) || {
    echo "reversedumpdir fail"
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
