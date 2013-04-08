
. ../lib_act_common.sh

arrange() {
  arrange_common
  (cd stage; arrange_dirofdump)
  (cd expected; arrange_dumpofdir)
}

act() {
  act_run_dumpdir "stage" "actual"
}
