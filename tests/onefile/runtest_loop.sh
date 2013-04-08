#! /bin/sh

set -e
set -u
set -x

. ./libruntest.sh

arrange_in_stage() {
  touch somefile
}

arrange_in_expected() {
  touch somefile
}

runtest_loop
