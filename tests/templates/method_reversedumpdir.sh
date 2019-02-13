
arrange_input() {
  arrange_dumpfile
}

arrange_expected() {
  arrange_dirs
}

act() {
  (
    cd actual
    dumpdir -r ../input/dumpfile
  ) || {
    exitstatus=$?
    echo "reversedumpdir fail with exitstatus $exitstatus"
    exit $exitstatus
  }
}
