#! /bin/sh

set -e
set -u
set -x

. ../libruntest.sh
. ../lib_method_loop.sh
. ./libonedir.sh

runtest
