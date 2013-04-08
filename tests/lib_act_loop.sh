
. ../lib_act_common.sh

act() {
  act_run_dumpdir "stage" "temp"
  act_run_reversedumpdir "temp" "actual"
}
