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

act_reversedumpdir() {
  act_run_reversedumpdir "stage" "actual"
}

act() {
  act_reversedumpdir
}

runtest
