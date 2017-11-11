
include(lib_data_common.sh)

content="\
some content
some more content
"

dumpfile="\
f somefile
$(echo -n "$content" | marklines)
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  echo -n "$content" > somefile
}
