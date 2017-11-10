#! /bin/sh

PATH="$PWD:$PATH"

cd tests
rm -rf actualtests
mkdir -p actualtests
for datafile in templates/*_data.sh; do
  for methodfile in templates/lib_method_*.sh; do
    datapart=${datafile%_*}
    methodpart=${methodfile##*_}
    sourcefilename=${datapart}_${methodpart}
    targetfilename=${sourcefilename/templates/actualtests}
    m4 -I templates $sourcefilename > $targetfilename
    chmod +x $targetfilename
  done
done
cd actualtests
shut
