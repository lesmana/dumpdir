
setuptestenvironment() {
  testenvironment="$0_environment"
  rm -rf "$testenvironment"
  mkdir "$testenvironment"
  cd "$testenvironment"
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
