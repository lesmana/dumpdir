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

arrange_in_stage() {
  arrange_in_stage_loop
}

arrange_in_expected() {
  arrange_in_expected_loop
}

runtest_loop
