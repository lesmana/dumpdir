
dumpfile="\
d dir1
d dir1/dir2
d dir1/dir2/dir3
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  mkdir dir1
  mkdir dir1/dir2
  mkdir dir1/dir2/dir3
}
