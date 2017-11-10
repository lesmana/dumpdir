
arrange() {
  mkdir stage
  mkdir actual
  mkdir expected
  (cd stage; arrange_in_stage) || exit
  (cd expected; arrange_in_expected) || exit
}

assert() {
  diff -r actual expected
}

runtest() {
  arrange
  act
  assert
}
