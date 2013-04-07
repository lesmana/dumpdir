#! /bin/sh

set -x

rm -rf workdir
mkdir workdir

(
  cd workdir
  touch somefile
  ../../../../dumpdir > ../actual
)

cat > expected << EOF
f somefile
EOF

diff actual expected
