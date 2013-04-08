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

  mkdir temp

  mkdir actual

  mkdir expected
  echo -n "$dumpfile" > expected/dumpfile
  echo 0 > expected/reversedumpdirexitstatus
  echo 0 > expected/dumpdirexitstatus
}

act() {
  (
    cd temp
    ../../../../reversedumpdir ../stage/dumpfile
    echo $? > ../actual/reversedumpdirexitstatus
  )

  (
    cd temp
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
