#! /bin/sh

set -e
set -u
set -x

. ./libruntest.sh
. ./libonefile.sh

arrange_in_stage_dumpdir() {
  arrange_dirofdump
}

arrange_in_expected_dumpdir() {
  arrange_dumpofdir
}

arrange_in_stage() {
  arrange_in_stage_dumpdir
}

arrange_in_expected() {
  arrange_in_expected_dumpdir
}

runtest_dumpdir
