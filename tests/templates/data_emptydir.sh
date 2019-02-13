
dumpfile="\
d emptydir
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  mkdir emptydir
}
