
include(lib_method.sh)

arrange_stage() {
  arrange_dirofdump
}

arrange_expected() {
  arrange_dumpofdir
}

act() {
  act_dumpdir
}
