
include(lib_method.sh)

arrange_in_stage() {
  arrange_dirofdump
}

arrange_in_expected() {
  arrange_dumpofdir
}

act() {
  act_run_dumpdir "stage" "actual"
}
