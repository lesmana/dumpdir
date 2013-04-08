
act_loop() {
  act_run_dumpdir "stage" "temp"
  act_run_reversedumpdir "temp" "actual"
}
