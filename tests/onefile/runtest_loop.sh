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

runtest_loop
