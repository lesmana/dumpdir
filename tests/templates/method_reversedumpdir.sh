
arrange_stage() {
  arrange_dumpofdir
}

arrange_expected() {
  arrange_dirofdump
}

act() {
  (
    cd actual
    dumpdir -r ../stage/dumpfile
  ) || {
    exitstatus=$?
    echo "reversedumpdir fail with exitstatus $exitstatus"
    exit $exitstatus
  }
}
