
arrange_dirofdump() {
  echo "you did not redefine arrange_dirofdump"
  echo "you lost the game"
  return 22
}

arrange_dumpofdir() {
  echo "you did not redefine arrange_dumpofdir"
  echo "you lost the game"
  return 22
}

act_run_dumpdir() {
  workdir=$1
  outputdir=$2
  (
    cd "$workdir"
    ../../../../dumpdir > ../"$outputdir"/dumpfile
  )
}

act_run_reversedumpdir() {
  inputdir=$1
  workdir=$2
  (
    cd "$workdir"
    ../../../../reversedumpdir ../"$inputdir"/dumpfile
  )
}
