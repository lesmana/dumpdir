#! /bin/sh

PATH="$PWD:$PATH"

cd tests
rm -rf actualtests
mkdir -p actualtests
for datafile in templates/data_*.sh; do
  for methodfile in templates/method_*.sh; do
    datapart=${datafile##*_}
    methodpart=${methodfile##*_}
    sourcefilename=test_${datapart}
    targetfilename=actualtests/test_${datapart%.sh}_${methodpart}
    m4 -I templates -DMETHOD=$methodfile $sourcefilename > $targetfilename
    chmod +x $targetfilename
  done
done
cd actualtests
shut
