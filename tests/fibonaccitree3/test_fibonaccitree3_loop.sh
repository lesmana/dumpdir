#! /bin/sh

set -e
set -u
set -x

. ../lib_runtest.sh
. ../lib_method_loop.sh
. ./test_fibonaccitree3_data.sh

runtest
