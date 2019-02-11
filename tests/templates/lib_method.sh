
act_dumpdir() {
  workdir=$1
  outputdir=$2
  (
    cd "$workdir"
    dumpdir > ../"$outputdir"/dumpfile
  ) || {
    exitstatus=$?
    echo "dumpdir fail with exitstatus $exitstatus"
    exit $exitstatus
  }
}

act_reversedumpdir() {
  inputdir=$1
  workdir=$2
  (
    cd "$workdir"
    dumpdir -r ../"$inputdir"/dumpfile
  ) || {
    exitstatus=$?
    echo "reversedumpdir fail with exitstatus $exitstatus"
    exit $exitstatus
  }
}
