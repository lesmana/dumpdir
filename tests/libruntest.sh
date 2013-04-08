
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

arrange_in_stage() {
  echo "you did not redefine arrange_in_stage"
  echo "you lost the game"
  return 22
}

arrange_in_expected() {
  echo "you did not redefine arrange_in_expected"
  echo "you lost the game"
  return 22
}

arrange() {
  arrange_common
  (cd stage; arrange_in_stage)
  (cd expected; arrange_in_expected)
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
