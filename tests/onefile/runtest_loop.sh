#! /bin/sh

set -x

. ./libruntest.sh

arrange() {
  mkdir stage
  touch stage/somefile

  mkdir temp

  mkdir actual

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

runtest
