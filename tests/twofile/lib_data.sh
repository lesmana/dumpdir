
dumpfile="\
f somefile1
f somefile2
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  touch somefile1
  touch somefile2
}
