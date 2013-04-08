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

runtest
