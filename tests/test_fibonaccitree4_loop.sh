#! /bin/sh

set -e
set -u
set -x

. ./lib_runtest.sh
. ./lib_method_loop.sh
. ./test_fibonaccitree4_data.sh

runtest
