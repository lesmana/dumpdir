#! /bin/sh

set -e
set -u
set -x

include(lib_runtest.sh)
include(lib_method_reverseloop.sh)
include(test_emptyfile2_data.sh)

runtest
