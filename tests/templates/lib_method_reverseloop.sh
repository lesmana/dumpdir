
include(lib_method.sh)

arrange_in_stage() {
  arrange_dumpofdir
}

arrange_in_expected() {
  arrange_dumpofdir
}

act() {
  mkdir temp
  act_run_reversedumpdir "stage" "temp"
  act_run_dumpdir "temp" "actual"
}