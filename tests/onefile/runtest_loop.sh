#! /bin/sh

set -e
set -u
set -x

. ./libruntest.sh
. ./libonefile.sh

arrange_in_stage_loop() {
  arrange_dirofdump
}

arrange_in_expected_loop() {
  arrange_dirofdump
}

runtest_loop
