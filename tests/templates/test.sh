#! /bin/sh

include(DATA)
include(METHOD)

arrange() {
  mkdir stage
  mkdir actual
  mkdir expected
  (
    cd stage
    arrange_stage
  ) || {
    exitstatus=$?
    echo "arange stage failed"
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
  diff -r actual expected
}

runtest() {
  arrange
  act
  assert
}

runtest
