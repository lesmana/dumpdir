
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
> some content1
> some more content1
f somefile2
> some content2
> some more content2
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  echo -n "$content1" > somefile1
  echo -n "$content2" > somefile2
}
