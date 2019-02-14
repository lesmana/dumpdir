#! /bin/sh

rm -rf generated
mkdir -p generated
for datafile in templates/data_*; do
  for methodfile in templates/method_*; do
    datapart=${datafile##*_}
    methodpart=${methodfile##*_}
    targetfile=generated/test_${datapart}_${methodpart}.sh
    m4 -I templates -DDATA=$datafile -DMETHOD=$methodfile test > $targetfile
    chmod +x $targetfile
  done
done
