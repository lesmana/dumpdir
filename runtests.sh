#! /bin/sh

PATH="$PWD:$PATH"

cd tests
rm -rf actualtests
mkdir -p actualtests
for datafile in templates/*_data.sh; do
  for methodfile in templates/lib_method_*.sh; do
    datapart=${datafile%_*}
    methodpart=${methodfile##*_}
    testfilename=${datapart}_${methodpart}
    cp -a $testfilename actualtests
  done
  cp -a $datafile actualtests
done
cp -a templates/lib_* actualtests
cd actualtests
shut -r
