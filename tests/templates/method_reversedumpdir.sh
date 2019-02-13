
arrange_input() {
  arrange_dumpofdir
}

arrange_expected() {
  arrange_dirofdump
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
