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

act() {
  inputdir="stage"
  workdir="actual"
  (
    cd "$workdir"
    ../../../../reversedumpdir ../"$inputdir"/dumpfile
    echo $? > ../actual/reversedumpdirexitstatus
  )
}

runtest
