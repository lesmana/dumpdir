
arrange() {
  mkdir stage
  mkdir actual
  mkdir expected
  (
    cd stage
    arrange_in_stage
  ) || {
    exitstatus=$?
    echo "arange in stage failed"
    exit $exitstatus
  }
  (
    cd expected
    arrange_in_expected
  ) || {
    exitstatus=$?
    echo "arange in expected failed"
    exit $exitstatus
  }
}

assert() {
  diff -r actual expected
}

runtest() {
  arrange
  act
  assert
}
