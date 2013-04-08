
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

assert() {
  diff -r actual expected
}

runtest_dumpdir() {
  setuptestenvironment
  arrange_dumpdir
  act_dumpdir
  assert
}

runtest_loop() {
  setuptestenvironment
  arrange_loop
  act_loop
  assert
}

runtest_reversedumpdir() {
  setuptestenvironment
  arrange_reversedumpdir
  act_reversedumpdir
  assert
}

runtest_reverseloop() {
  setuptestenvironment
  arrange_reverseloop
  act_reverseloop
  assert
}
