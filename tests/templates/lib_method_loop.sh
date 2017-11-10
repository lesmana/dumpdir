
include(lib_method.sh)

arrange_stage() {
  arrange_dirofdump
}

arrange_expected() {
  arrange_dirofdump
}

act() {
  mkdir temp
  act_dumpdir "stage" "temp"
  act_reversedumpdir "temp" "actual"
}
