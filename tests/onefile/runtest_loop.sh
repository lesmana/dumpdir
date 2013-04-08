#! /bin/sh

set -e
set -u
set -x

. ./libruntest.sh

arrange_stage() {
  touch stage/somefile
}

arrange_expected() {
  touch expected/somefile
  echo 0 > expected/dumpdirexitstatus
  echo 0 > expected/reversedumpdirexitstatus
}

arrange() {
  mkdir stage
  arrange_stage

  mkdir temp

  mkdir actual

  mkdir expected
  arrange_expected
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
