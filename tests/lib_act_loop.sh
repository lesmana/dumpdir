
. ../lib_act_common.sh

arrange_in_stage() {
  arrange_dirofdump
}

arrange_in_expected() {
  arrange_dirofdump
}

arrange() {
  arrange_common
  (cd stage; arrange_in_stage)
  (cd expected; arrange_in_expected)
}

act() {
  act_run_dumpdir "stage" "temp"
  act_run_reversedumpdir "temp" "actual"
}
