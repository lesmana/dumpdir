#! /bin/sh

set -e
set -u
set -x

. ./lib_runtest.sh
. ./lib_method_reversedumpdir.sh
. ./test_somefile2_data.sh

runtest
