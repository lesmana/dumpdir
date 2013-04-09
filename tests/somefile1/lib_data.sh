
content="\
some content
some more content
"

marklines() {
  while read line; do
    echo "> $line"
  done
}

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
