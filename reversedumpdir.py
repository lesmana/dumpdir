#! /usr/bin/env python

import os
import sys

# ------------------------------------------------------------------------------
class ReverseDumpDir(object):

  def __init__(self, osmod, openfunc):
    self.osmod = osmod
    self.openfunc = openfunc

  def reversedumpdir(self, inputfile):
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

# ------------------------------------------------------------------------------
class Main(object):

  def __init__(self):
    pass

  def filenamefromargv(self, argv):
    if len(argv) == 2:
      inputfilename = argv[1]
    else:
      raise Exception('need filename')
    return inputfilename

  def parsefileandcreatedirs(self, inputfilename):
    with open(inputfilename) as inputfile:
      reversedumpdir = ReverseDumpDir(os, open)
      reversedumpdir.reversedumpdir(inputfile)

  def runexcept(self, argv):
    inputfilename = self.filenamefromargv(argv)
    self.parsefileandcreatedirs(inputfilename)

  def run(self, argv, stdout, stderr):
    try:
      self.runexcept(argv)
      return 0
    except Exception as error:
      stdout.write('ERROR: %s\n' % str(error))
      return 1

# ------------------------------------------------------------------------------
def main():
  mainrunner = Main()
  exitstatus = mainrunner.run(sys.argv, sys.stdout, sys.stderr)
  sys.exit(exitstatus)
