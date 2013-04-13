
dumpfile="\
f dir0
d dir1
d dir2
f dir2/dir0
d dir2/dir1
d dir3
d dir3/dir1
d dir3/dir2
f dir3/dir2/dir0
d dir3/dir2/dir1
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  touch dir0
  mkdir dir1
  mkdir dir2
  touch dir2/dir0
  mkdir dir2/dir1
  mkdir dir3
  mkdir dir3/dir1
  mkdir dir3/dir2
  touch dir3/dir2/dir0
  mkdir dir3/dir2/dir1
}
