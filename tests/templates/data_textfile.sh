
content="\
hello
world
"

dumpfile="\
f textfile
> hello
> world
"

arrange_dumpofdir() {
  echo -n "$dumpfile" > dumpfile
}

arrange_dirofdump() {
  echo -n "$content" > textfile
}
