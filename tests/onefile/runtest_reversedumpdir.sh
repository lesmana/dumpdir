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
  echo -n "$dumpfile" > stage/dumpfile

  rm -rf actual
  mkdir actual

  rm -rf expected
  mkdir expected
  touch expected/somefile
  echo 0 > expected/reversedumpdirexitstatus
}

act() {
  (
    cd actual
    ../../../../reversedumpdir ../stage/dumpfile
    echo $? > ../actual/reversedumpdirexitstatus
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
