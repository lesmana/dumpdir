#! /bin/sh

set -e
set -u
set -x

. ../libruntest.sh
. ../lib_act_loop.sh
. ./libonedir.sh

runtest_loop
