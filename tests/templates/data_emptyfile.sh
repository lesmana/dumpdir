
dumpfile="\
f emptyfile
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  touch emptyfile
}
