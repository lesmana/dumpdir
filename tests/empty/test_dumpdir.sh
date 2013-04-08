#! /bin/sh

set -e
set -u
set -x

. ../libruntest.sh
. ../lib_act_dumpdir.sh
. ./libempty.sh

runtest_dumpdir
