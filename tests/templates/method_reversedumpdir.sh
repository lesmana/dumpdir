
include(lib_method.sh)

arrange_stage() {
  arrange_dumpofdir
}

arrange_expected() {
  arrange_dirofdump
}

act() {
  act_reversedumpdir
}
