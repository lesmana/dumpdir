#! /bin/sh

set -e
set -u
set -x

. ../lib_runtest.sh
. ../lib_method_dumpdir.sh
. ./lib_data.sh

runtest
