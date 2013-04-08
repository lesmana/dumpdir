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

act() {
  workdir="stage"
  outputdir="temp"
  (
    cd "$workdir"
    ../../../../dumpdir > ../"$outputdir"/dumpfile
    echo $? > ../actual/dumpdirexitstatus
  )

  inputdir="temp"
  workdir="actual"
  (
    cd "$workdir"
    ../../../../reversedumpdir ../"$inputdir"/dumpfile
    echo $? > ../actual/reversedumpdirexitstatus
  )
}

runtest
