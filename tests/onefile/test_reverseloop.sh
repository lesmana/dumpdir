#! /bin/sh

set -e
set -u
set -x

. ../libruntest.sh
. ../lib_method_reverseloop.sh
. ./lib_data.sh

runtest
