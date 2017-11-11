
content="\
some content
some more content
"

dumpfile="\
f somefile
> some content
> some more content
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  echo -n "$content" > somefile
}
