
. ../lib_act_common.sh

arrange() {
  arrange_common
  (cd stage; arrange_dirofdump)
  (cd expected; arrange_dirofdump)
}

act() {
  act_run_dumpdir "stage" "temp"
  act_run_reversedumpdir "temp" "actual"
}
