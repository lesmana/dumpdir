
include(lib_method.sh)

arrange_in_stage() {
  arrange_dirofdump
}

arrange_in_expected() {
  arrange_dirofdump
}

act() {
  mkdir temp
  act_run_dumpdir "stage" "temp"
  act_run_reversedumpdir "temp" "actual"
}