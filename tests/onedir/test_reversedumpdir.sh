#! /bin/sh

set -e
set -u
set -x

. ../libruntest.sh
. ../lib_act_reversedumpdir.sh
. ./libonedir.sh

runtest
