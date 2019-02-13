
arrange_input() {
  arrange_dirs
}

arrange_expected() {
  arrange_dumpfile
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
