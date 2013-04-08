#! /bin/sh

set -e
set -u
set -x

. ../libruntest.sh
. ./libonedir.sh

runtest_loop
