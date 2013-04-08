
. ../lib_act_common.sh

arrange_reversedumpdir() {
  arrange_common
  (cd stage; arrange_dumpofdir)
  (cd expected; arrange_dirofdump)
}

act() {
  act_run_reversedumpdir "stage" "actual"
}
