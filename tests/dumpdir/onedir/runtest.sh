#! /bin/sh

set -x

rm -rf workdir
mkdir workdir

(
  cd workdir
  mkdir somedir
  ../../../../dumpdir > ../actual
)

cat > expected << EOF
d somedir
EOF

diff actual expected
