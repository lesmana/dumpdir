#! /usr/bin/env python

import os
import sys

# ------------------------------------------------------------------------------
def main():
  if len(sys.argv) == 2:
    inputfilename = sys.argv[1]
  else:
    print 'need filename'
    sys.exit(1)

  with open(inputfilename) as inputfile:
    for line in inputfile:
      line = line.strip()
      if not line:
        continue
      type, _, name = line.partition(' ')
      if type == 'd':
        currentfilename = None
        os.mkdir(name)
      elif type == 'f':
        currentfilename = name
        currentfile = open(currentfilename, 'w')
        currentfile.close()
      elif type == '>':
        currentfile = open(currentfilename, 'a')
        currentfile.write(name + '\n')
        currentfile.close()
      else:
        raise Exception('unknown type: %s' % type)
