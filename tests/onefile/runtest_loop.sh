#! /bin/sh

set -e
set -u
set -x

. ./libruntest.sh

arrange_dirofdump() {
  touch somefile
}

arrange_in_stage() {
  arrange_dirofdump
}

arrange_in_expected() {
  arrange_dirofdump
}

runtest_loop
