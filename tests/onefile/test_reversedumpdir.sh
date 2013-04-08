#! /bin/sh

set -e
set -u
set -x

. ../libruntest.sh
. ../lib_method_reversedumpdir.sh
. ./libonefile.sh

runtest
