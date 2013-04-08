
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

arrange_dumpdir() {
  arrange_common
  (cd stage; arrange_dirofdump)
  (cd expected; arrange_dumpofdir)
}

arrange_loop() {
  arrange_common
  (cd stage; arrange_dirofdump)
  (cd expected; arrange_dirofdump)
}

arrange_reversedumpdir() {
  arrange_common
  (cd stage; arrange_dumpofdir)
  (cd expected; arrange_dirofdump)
}

arrange_reverseloop() {
  arrange_common
  (cd stage; arrange_dumpofdir)
  (cd expected; arrange_dumpofdir)
}

act() {
  echo "you did not redefine act"
  echo "you lost the game"
  return 22
}

assert() {
  diff -r actual expected
}

runtest_dumpdir() {
  setuptestenvironment
  arrange_dumpdir
  act
  assert
}

runtest_loop() {
  setuptestenvironment
  arrange_loop
  act
  assert
}

runtest_reversedumpdir() {
  setuptestenvironment
  arrange_reversedumpdir
  act
  assert
}

runtest_reverseloop() {
  setuptestenvironment
  arrange_reverseloop
  act
  assert
}
