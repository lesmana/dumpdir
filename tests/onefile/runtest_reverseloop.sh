#! /bin/sh

set -e
set -u
set -x

. ./libruntest.sh
. ./libonefile.sh

arrange_in_stage_reverseloop() {
  arrange_dumpofdir
}

arrange_in_expected_reverseloop() {
  arrange_dumpofdir
}

arrange_in_stage() {
  arrange_in_stage_reverseloop
}

arrange_in_expected() {
  arrange_in_expected_reverseloop
}

runtest_reverseloop
