
setuptestenvironment() {
  testenvironment="$0_environment"
  rm -rf "$testenvironment"
  mkdir "$testenvironment"
  cd "$testenvironment"
}

arrange_dumpdir() {
  mkdir stage
  mkdir temp
  mkdir actual
  mkdir expected
  (cd stage; arrange_in_stage_dumpdir)
  (cd expected; arrange_in_expected_dumpdir)
}

arrange_loop() {
  mkdir stage
  mkdir temp
  mkdir actual
  mkdir expected
  (cd stage; arrange_in_stage_loop)
  (cd expected; arrange_in_expected_loop)
}

arrange_reversedumpdir() {
  mkdir stage
  mkdir temp
  mkdir actual
  mkdir expected
  (cd stage; arrange_in_stage_reversedumpdir)
  (cd expected; arrange_in_expected_reversedumpdir)
}

arrange_reverseloop() {
  mkdir stage
  mkdir temp
  mkdir actual
  mkdir expected
  (cd stage; arrange_in_stage_reverseloop)
  (cd expected; arrange_in_expected_reverseloop)
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
