
dumpfile="\
d dir
d dir/dir
d dir/dir/dir
d dir/dir/dir/dir
f dir/dir/dir/dir/file
> foo
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  mkdir -p dir/dir/dir/dir
  echo foo > dir/dir/dir/dir/file
}
