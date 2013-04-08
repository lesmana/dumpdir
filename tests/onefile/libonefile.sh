
dumpfile="\
f somefile
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  touch somefile
}
