#! /bin/sh

set -e
set -u
set -x

include(lib_runtest.sh)
include(lib_method_loop.sh)
include(test_empty_data.sh)

runtest
