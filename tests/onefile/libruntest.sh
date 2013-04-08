
setuptestenvironment() {
  testenvironment="$0_environment"
  rm -rf "$testenvironment"
  mkdir "$testenvironment"
  cd "$testenvironment"
}

arrange_common() {
  mkdir stage
  mkdir temp
  mkdir actual
  mkdir expected
}

arrange_dumpdir() {
  arrange_common
  (cd stage; arrange_dirofdump)
  (cd expected; arrange_dumpofdir)
}

arrange_loop() {
  arrange_common
  (cd stage; arrange_dirofdump)
  (cd expected; arrange_dirofdump)
}

arrange_reversedumpdir() {
  arrange_common
  (cd stage; arrange_dumpofdir)
  (cd expected; arrange_dirofdump)
}

arrange_reverseloop() {
  arrange_common
  (cd stage; arrange_dumpofdir)
  (cd expected; arrange_dumpofdir)
}

act_run_dumpdir() {
  workdir=$1
  outputdir=$2
  (
    cd "$workdir"
    ../../../../dumpdir > ../"$outputdir"/dumpfile
  )
}

act_run_reversedumpdir() {
  inputdir=$1
  workdir=$2
  (
    cd "$workdir"
    ../../../../reversedumpdir ../"$inputdir"/dumpfile
  )
}

act_dumpdir() {
  act_run_dumpdir "stage" "actual"
}

act_loop() {
  act_run_dumpdir "stage" "temp"
  act_run_reversedumpdir "temp" "actual"
}

act_reversedumpdir() {
  act_run_reversedumpdir "stage" "actual"
}

act_reverseloop() {
  act_run_reversedumpdir "stage" "temp"
  act_run_dumpdir "temp" "actual"
}

assert() {
  diff -r actual expected
}

runtest_dumpdir() {
  setuptestenvironment
  arrange_dumpdir
  act_dumpdir
  assert
}

runtest_loop() {
  setuptestenvironment
  arrange_loop
  act_loop
  assert
}

runtest_reversedumpdir() {
  setuptestenvironment
  arrange_reversedumpdir
  act_reversedumpdir
  assert
}

runtest_reverseloop() {
  setuptestenvironment
  arrange_reverseloop
  act_reverseloop
  assert
}
