
dumpfile="\
d mt
f mt/ff
> foo
d mt/sd1
f mt/sd1/fg
> bar
d mt/sd2
f mt/sd2/fh
> baz
d mt/xd
d mt/xd/sde
d mt/xd/sdf
f mt/xd/sdf/fe
> wat
"

arrange_dumpfile() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirs() {
  mkdir mt
  echo foo > mt/ff
  mkdir mt/sd1
  echo bar > mt/sd1/fg
  mkdir mt/sd2
  echo baz > mt/sd2/fh
  mkdir mt/xd
  mkdir mt/xd/sde
  mkdir mt/xd/sdf
  echo wat > mt/xd/sdf/fe
}
