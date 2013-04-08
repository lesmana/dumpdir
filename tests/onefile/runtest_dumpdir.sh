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

act() {
  act_run_dumpdir "stage" "actual"
}

runtest
