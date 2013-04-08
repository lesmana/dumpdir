#! /bin/sh

set -x

dumpfile="\
f somefile
"

setuptestenvironment() {
  testenvironment="$0_environment"
  rm -rf "$testenvironment"
  mkdir "$testenvironment"
  cd "$testenvironment"
}

arrange() {
  rm -rf stage
  mkdir stage
  touch stage/somefile

  rm -rf actual
  mkdir actual

  rm -rf expected
  mkdir expected
  echo -n "$dumpfile" > expected/dumpfile
  echo 0 > expected/dumpdirexitstatus
}

act() {
  (
    cd stage
    ../../../../dumpdir > ../actual/dumpfile
    echo $? > ../actual/dumpdirexitstatus
  )
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
