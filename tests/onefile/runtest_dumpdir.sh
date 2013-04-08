#! /bin/sh

set -e
set -u
set -x

. ./libruntest.sh

dumpfile="\
f somefile
"

arrange_stage() {
  touch stage/somefile
}

arrange_expected() {
  echo -n "$dumpfile" > expected/dumpfile
  echo 0 > expected/dumpdirexitstatus
}

arrange() {
  mkdir stage
  arrange_stage

  mkdir actual

  mkdir expected
  arrange_expected
}

act() {
  (
    cd stage
    ../../../../dumpdir > ../actual/dumpfile
    echo $? > ../actual/dumpdirexitstatus
  )
}

runtest
