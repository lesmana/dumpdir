#! /bin/sh

set -e
set -u
set -x

. ../lib_runtest.sh
. ../lib_method_loop.sh
. ./lib_data.sh

runtest
