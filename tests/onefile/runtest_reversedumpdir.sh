#! /bin/sh

set -e
set -u
set -x

. ./libruntest.sh

dumpfile="\
f somefile
"

arrange_in_stage() {
  echo -n "$dumpfile" > dumpfile
}

arrange_in_expected() {
  touch somefile
}

runtest_reversedumpdir
