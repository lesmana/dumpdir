
setuptestenvironment() {
  testenvironment="$0_environment"
  rm -rf "$testenvironment"
  mkdir "$testenvironment"
  cd "$testenvironment"
}

arrange_common() {
  mkdir stage
  mkdir temp
  mkdir actual
  mkdir expected
}

arrange() {
  echo "you did not redefine arrange"
  echo "you lost the game"
  return 22
}

act() {
  echo "you did not redefine act"
  echo "you lost the game"
  return 22
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
