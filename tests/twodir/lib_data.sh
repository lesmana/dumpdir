
dumpfile="\
d somedir1
d somedir2
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  mkdir somedir1
  mkdir somedir2
}
