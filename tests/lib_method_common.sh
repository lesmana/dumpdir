
act_run_dumpdir() {
  workdir=$1
  outputdir=$2
  (
    cd "$workdir"
    ../../../../dumpdir > ../"$outputdir"/dumpfile
  ) || exit
}

act_run_reversedumpdir() {
  inputdir=$1
  workdir=$2
  (
    cd "$workdir"
    ../../../../reversedumpdir ../"$inputdir"/dumpfile
  ) || exit
}
