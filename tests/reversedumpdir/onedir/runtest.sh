#! /bin/sh

set -x

rm -rf actual
rm -rf expected

cat > inputfile << EOF
d somedir
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
mkdir expected/somedir

diff -r actual expected
