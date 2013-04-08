#! /bin/sh

set -e
set -u
set -x

. ./libruntest.sh

dumpfile="\
f somefile
"

arrange_stage() {
  echo -n "$dumpfile" > stage/dumpfile
}

arrange_expected() {
  touch expected/somefile
  echo 0 > expected/reversedumpdirexitstatus
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
    cd actual
    ../../../../reversedumpdir ../stage/dumpfile
    echo $? > ../actual/reversedumpdirexitstatus
  )
}

runtest
