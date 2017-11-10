
include(lib_method.sh)

arrange_stage() {
  arrange_dumpofdir
}

arrange_expected() {
  arrange_dumpofdir
}

act() {
  mkdir temp
  act_reversedumpdir "stage" "temp"
  act_dumpdir "temp" "actual"
}
