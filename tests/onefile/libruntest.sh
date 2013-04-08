
setuptestenvironment() {
  testenvironment="$0_environment"
  rm -rf "$testenvironment"
  mkdir "$testenvironment"
  cd "$testenvironment"
}

arrange() {
  mkdir stage
  (cd stage; arrange_in_stage)

  mkdir temp

  mkdir actual

  mkdir expected
  (cd expected; arrange_in_expected)
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
  arrange
  act_dumpdir
  assert
}

runtest_loop() {
  setuptestenvironment
  arrange
  act_loop
  assert
}

runtest_reversedumpdir() {
  setuptestenvironment
  arrange
  act_reversedumpdir
  assert
}

runtest_reverseloop() {
  setuptestenvironment
  arrange
  act_reverseloop
  assert
}
