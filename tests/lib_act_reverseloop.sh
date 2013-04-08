
. ../lib_act_common.sh

arrange_reverseloop() {
  arrange_common
  (cd stage; arrange_dumpofdir)
  (cd expected; arrange_dumpofdir)
}

act() {
  act_run_reversedumpdir "stage" "temp"
  act_run_dumpdir "temp" "actual"
}
