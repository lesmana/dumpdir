
dumpfile="\
d dir0
d dir0/dir1
d dir0/dir2
d dir0/dir2/dir3
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  mkdir dir0
  mkdir dir0/dir1
  mkdir dir0/dir2
  mkdir dir0/dir2/dir3
}
