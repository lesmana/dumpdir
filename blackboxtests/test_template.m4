#! /bin/sh

include(DATA)
include(METHOD)

arrange() {
  mkdir input
  mkdir actual
  mkdir expected
  (
    cd input
    arrange_input
  ) || {
    exitstatus=$?
    echo "arange input failed"
    exit $exitstatus
  }
  (
    cd expected
    arrange_expected
  ) || {
    exitstatus=$?
    echo "arange expected failed"
    exit $exitstatus
  }
}

assert() {
  diff -r --no-dereference actual expected
}

runtest() {
  arrange
  act
  assert
}

runtest
