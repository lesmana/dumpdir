#! /bin/sh

set -e
set -u
set -x

. ./libruntest.sh

dumpfile="\
f somefile
"

arrange_dirofdump() {
  touch somefile
}

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_in_stage() {
  arrange_dirofdump
}

arrange_in_expected() {
  arrange_dumpofdir
}

runtest_dumpdir
