#! /bin/sh

set -e
set -u
set -x

. ../libruntest.sh
. ./libempty.sh

runtest_reversedumpdir
