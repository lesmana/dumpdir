#! /bin/sh

PATH="$PWD:$PATH"

cd tests
rm -rf actualtests
mkdir -p actualtests
for datafile in templates/*_data.sh; do
  for methodfile in templates/lib_method_*.sh; do
    datapart=${datafile%_*}
    methodpart=${methodfile##*_}
    methodname=${methodpart%.sh}
    sourcefilename=${datapart}.sh
    targetfilename=${datapart/templates/actualtests}_${methodpart}
    m4 -I templates -DMETHOD=$methodname $sourcefilename > $targetfilename
    chmod +x $targetfilename
  done
done
cd actualtests
shut
