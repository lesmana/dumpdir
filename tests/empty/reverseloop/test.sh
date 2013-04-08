#! /bin/sh

set -x

rm -rf workdir
mkdir workdir

cat > orig <<EOF
EOF

(
  cd workdir
  ../../../../reversedumpdir ../orig
) || {
  echo "reversedumpdir fail"
  exit 1
}

(
  cd workdir
  ../../../../dumpdir > ../copy
) || {
  echo "dumpdir fail"
  exit 1
}

diff -r orig copy
