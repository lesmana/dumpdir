
setuptestenvironment() {
  testenvironment="$0_environment"
  rm -rf "$testenvironment"
  mkdir "$testenvironment"
  cd "$testenvironment"
}

arrange() {
  mkdir stage
  arrange_stage

  mkdir temp

  mkdir actual

  mkdir expected
  arrange_expected
}

act_run_dumpdir() {
  workdir=$1
  outputdir=$2
  (
    cd "$workdir"
    ../../../../dumpdir > ../"$outputdir"/dumpfile
    echo $? > ../actual/dumpdirexitstatus
  )
}

act_run_reversedumpdir() {
  inputdir=$1
  workdir=$2
  (
    cd "$workdir"
    ../../../../reversedumpdir ../"$inputdir"/dumpfile
    echo $? > ../actual/reversedumpdirexitstatus
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

runtest() {
  setuptestenvironment
  arrange
  act
  assert
}
