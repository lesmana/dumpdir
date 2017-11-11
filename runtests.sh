#! /bin/sh

PATH="$PWD:$PATH"

cd tests
rm -rf actualtests
mkdir -p actualtests
for datafile in templates/*_data.sh; do
  for methodfile in templates/method_*.sh; do
    datapart=${datafile%_*}
    methodpart=${methodfile##*_}
    sourcefilename=${datapart}.sh
    targetfilename=${datapart/templates/actualtests}_${methodpart}
    m4 -I templates -DMETHOD=$methodfile $sourcefilename > $targetfilename
    chmod +x $targetfilename
  done
done
cd actualtests
shut
