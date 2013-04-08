
. ../lib_method_common.sh

arrange_in_stage() {
  arrange_dumpofdir
}

arrange_in_expected() {
  arrange_dirofdump
}

act() {
  act_run_reversedumpdir "stage" "actual"
}
