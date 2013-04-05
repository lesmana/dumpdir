#! /bin/sh

set -x

rm -rf workdir
mkdir workdir

(
  cd workdir
  ../../../../dumpdir > ../actual
)

cat > expected << EOF
EOF

diff actual expected
