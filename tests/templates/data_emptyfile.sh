
dumpfile="\
f emptyfile
"

arrange_dumpfile() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirs() {
  touch emptyfile
}
