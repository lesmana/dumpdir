
. ../lib_data_common.sh

content1="\
some content1
some more content1
"

content2="\
some content2
some more content2
"

dumpfile="\
f somefile1
$(echo -n "$content1" | marklines)
f somefile2
$(echo -n "$content2" | marklines)
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  echo -n "$content1" > somefile1
  echo -n "$content2" > somefile2
}
