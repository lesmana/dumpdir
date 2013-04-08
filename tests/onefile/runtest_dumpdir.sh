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

runtest_dumpdir
