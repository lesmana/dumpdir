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
  mkdir stage
  echo -n "$dumpfile" > stage/dumpfile

  mkdir actual

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
  setuptestenvironment
  arrange
  act
  assert
}

runtest
