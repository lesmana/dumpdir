#! /bin/sh

set -x

inputfile="\
f somefile
"

setuptestenvironment() {
  testenvironment="$0_environment"
  rm -rf "$testenvironment"
  mkdir "$testenvironment"
  cd "$testenvironment"
}

arrange() {
  rm -rf actual
  rm -rf expected

  echo -n "$inputfile" > inputfile

  mkdir expected
  touch expected/somefile

  mkdir actual
}

act() {
  (
    cd actual
    ../../../../reversedumpdir ../inputfile
  ) || {
    echo "fail"
    exit 1
  }
}

assert() {
  diff -r actual expected
}

runtest() {
  arrange
  act
  assert
}

setuptestenvironment
runtest
