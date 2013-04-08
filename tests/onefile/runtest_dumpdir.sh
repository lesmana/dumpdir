#! /bin/sh

set -x

. ./libruntest.sh

dumpfile="\
f somefile
"

arrange() {
  mkdir stage
  touch stage/somefile

  mkdir actual

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

runtest
