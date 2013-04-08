#! /bin/sh

set -e
set -u
set -x

. ../libruntest.sh
. ../lib_method_dumpdir.sh
. ./libonedir.sh

runtest
