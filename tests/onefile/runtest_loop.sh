#! /bin/sh

set -x

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

  rm -rf temp
  mkdir temp

  rm -rf actual
  mkdir actual

  rm -rf expected
  mkdir expected
  touch expected/somefile
  echo 0 > expected/dumpdirexitstatus
  echo 0 > expected/reversedumpdirexitstatus
}

act() {
  (
    cd stage
    ../../../../dumpdir > ../temp/dumpfile
    echo $? > ../actual/dumpdirexitstatus
  )

  (
    cd actual
    ../../../../reversedumpdir ../temp/dumpfile
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
