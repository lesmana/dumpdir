#! /bin/sh

set -e
set -u
set -x

. ./libruntest.sh
. ./libonefile.sh

runtest_reverseloop
