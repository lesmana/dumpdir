
act_dumpdir() {
  (
    cd stage
    dumpdir > ../actual/dumpfile
  ) || {
    exitstatus=$?
    echo "dumpdir fail with exitstatus $exitstatus"
    exit $exitstatus
  }
}

act_reversedumpdir() {
  (
    cd actual
    dumpdir -r ../stage/dumpfile
  ) || {
    exitstatus=$?
    echo "reversedumpdir fail with exitstatus $exitstatus"
    exit $exitstatus
  }
}
