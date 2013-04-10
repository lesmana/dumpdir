
dumpfile="\
d dir0
d dir0/dir1
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  mkdir dir0
  mkdir dir0/dir1
}
