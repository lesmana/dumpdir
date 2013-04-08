#! /bin/sh

set -e
set -u
set -x

. ../libruntest.sh
. ../lib_act_reverseloop.sh
. ./libempty.sh

runtest_reverseloop
