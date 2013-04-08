#! /bin/sh

set -e
set -u
set -x

. ./libruntest.sh

dumpfile="\
f somefile
"

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

runtest
