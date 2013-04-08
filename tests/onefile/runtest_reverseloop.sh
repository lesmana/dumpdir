#! /bin/sh

set -e
set -u
set -x

. ./libruntest.sh
. ./libonefile.sh

arrange_in_stage() {
  arrange_dumpofdir
}

arrange_in_expected() {
  arrange_dumpofdir
}

runtest_reverseloop
