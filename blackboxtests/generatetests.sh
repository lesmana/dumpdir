#! /bin/sh

rm -rf generated
mkdir -p generated
for datafile in data_*; do
  for methodfile in method_*; do
    targetfile=generated/test_${datafile#data_}_${methodfile#method_}.sh
    m4 -DDATA=$datafile -DMETHOD=$methodfile test > $targetfile
    chmod +x $targetfile
  done
done
