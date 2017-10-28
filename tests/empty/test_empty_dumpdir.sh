#! /bin/sh

set -e
set -u
set -x

. ./lib_runtest.sh
. ./lib_method_dumpdir.sh
. ./test_empty_data.sh

runtest
