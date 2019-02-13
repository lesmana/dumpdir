
dumpfile="\
d dir
d dir/dir
d dir/dir/dir
d dir/dir/dir/dir
f dir/dir/dir/dir/file
> foo
"

arrange_dumpfile() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirs() {
  mkdir -p dir/dir/dir/dir
  echo foo > dir/dir/dir/dir/file
}
