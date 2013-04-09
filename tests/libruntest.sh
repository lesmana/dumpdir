
setuptestenvironment() {
  testenvironment="$0_environment"
  rm -rf "$testenvironment"
  mkdir "$testenvironment"
  cd "$testenvironment"
}

arrange() {
  mkdir stage
  mkdir temp
  mkdir actual
  mkdir expected
  (cd stage; arrange_in_stage)
  (cd expected; arrange_in_expected)
}

assert() {
  diff -r actual expected
}

runtest() {
  setuptestenvironment
  arrange
  act
  assert
}
