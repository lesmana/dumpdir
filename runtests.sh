#! /bin/sh

PATH="$PWD:$PWD/tests/helpers:$PATH"

cd tests
rm -rf actualtests
mkdir -p actualtests
for datafile in templates/data_*.sh; do
  for methodfile in templates/method_*.sh; do
    datapart=${datafile##*_}
    methodpart=${methodfile##*_}
    targetfile=actualtests/test_${datapart%.sh}_${methodpart}
    m4 -I templates -DDATA=$datafile -DMETHOD=$methodfile test.sh > $targetfile
    chmod +x $targetfile
  done
done
cd actualtests
shut
