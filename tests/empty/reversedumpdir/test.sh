#! /bin/sh

set -x

rm -rf actual
rm -rf expected

cat > inputfile << EOF
EOF

(
  mkdir actual
  cd actual
  ../../../../reversedumpdir ../inputfile
) || {
  echo "fail"
  exit 1
}

mkdir expected

diff -r actual expected
