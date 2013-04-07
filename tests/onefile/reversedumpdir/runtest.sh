#! /bin/sh

set -x

rm -rf actual
rm -rf expected

cat > inputfile << EOF
f somefile
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
touch expected/somefile

diff -r actual expected
