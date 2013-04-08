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

act_loop() {
  act_run_dumpdir "stage" "temp"
  act_run_reversedumpdir "temp" "actual"
}

act() {
  act_loop
}

runtest
