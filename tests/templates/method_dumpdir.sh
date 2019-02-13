
arrange_stage() {
  arrange_dirofdump
}

arrange_expected() {
  arrange_dumpofdir
}

act() {
  (
    cd stage
    dumpdir > ../actual/dumpfile
  ) || {
    exitstatus=$?
    echo "dumpdir fail with exitstatus $exitstatus"
    exit $exitstatus
  }
}
