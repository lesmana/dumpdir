
arrange_input() {
  arrange_dirofdump
}

arrange_expected() {
  arrange_dumpofdir
}

act() {
  (
    cd input
    dumpdir > ../actual/dumpfile
  ) || {
    exitstatus=$?
    echo "dumpdir fail with exitstatus $exitstatus"
    exit $exitstatus
  }
}
