#! /bin/sh

set -e
set -u
set -x

. ../lib_runtest.sh
. ../lib_method_reversedumpdir.sh
. ./test_fibonaccitree4_data.sh

runtest
