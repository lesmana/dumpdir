#! /bin/sh

set -e
set -u
set -x

. ../libruntest.sh
. ../lib_act_dumpdir.sh
. ./libonedir.sh

runtest
