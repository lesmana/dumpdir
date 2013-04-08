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
  act_reversedumpdir
}

runtest
