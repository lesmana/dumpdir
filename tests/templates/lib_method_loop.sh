
. ./lib_method_common.sh

arrange_in_stage() {
  arrange_dirofdump
}

arrange_in_expected() {
  arrange_dirofdump
}

act() {
  act_run_dumpdir "stage" "temp"
  act_run_reversedumpdir "temp" "actual"
}
