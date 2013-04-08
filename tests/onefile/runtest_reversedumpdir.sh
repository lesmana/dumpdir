#! /bin/sh

set -e
set -u
set -x

. ./libruntest.sh
. ./libonefile.sh

arrange_in_stage_reversedumpdir() {
  arrange_dumpofdir
}

arrange_in_expected_reversedumpdir() {
  arrange_dirofdump
}

runtest_reversedumpdir
