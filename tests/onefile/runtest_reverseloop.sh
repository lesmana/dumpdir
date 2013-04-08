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
  inputdir="stage"
  workdir="temp"
  (
    cd "$workdir"
    ../../../../reversedumpdir ../"$inputdir"/dumpfile
    echo $? > ../actual/reversedumpdirexitstatus
  )

  workdir="temp"
  outputdir="actual"
  (
    cd "$workdir"
    ../../../../dumpdir > ../"$outputdir"/dumpfile
    echo $? > ../actual/dumpdirexitstatus
  )
}

runtest
