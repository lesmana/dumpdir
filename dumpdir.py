#! /usr/bin/env python

import os
import sys

# ------------------------------------------------------------------------------
class DumpDir(object):

  def dumpdir(self):
    cwd = os.getcwd()
    for (dirpath, dirnames, filenames) in os.walk(cwd):
      dirnames.sort()
      if dirpath != cwd:
        relpath = os.path.relpath(dirpath)
        sys.stdout.write('d %s\n' % (relpath))
      for filename in sorted(filenames):
        dirpath_filename = os.path.join(dirpath, filename)
        relpath_filename = os.path.relpath(dirpath_filename)
        if os.path.islink(relpath_filename):
          target = os.readlink(relpath_filename)
          commonprefix = os.path.commonprefix([cwd, target])
          if commonprefix != '/':
            target = '(...)' + os.path.relpath(target)
          sys.stdout.write('l %s -> %s\n' % (relpath_filename, target))
        else:
          sys.stdout.write('f %s\n' % (relpath_filename))
          with open(relpath_filename) as fileobject:
            for line in fileobject:
              sys.stdout.write('> %s\n' % (line.rstrip('\n')))

  def runexcept(self, argv):
    self.dumpdir()

# ------------------------------------------------------------------------------
class ReverseDumpDir(object):

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

  def filenamefromargv(self, argv):
    if len(argv) == 2:
      inputfilename = argv[1]
    else:
      raise Exception('need filename')
    return inputfilename

  def parsefileandcreatedirs(self, inputfilename):
    with open(inputfilename) as inputfile:
      self.reversedumpdir(inputfile)

  def runexcept(self, argv):
    inputfilename = self.filenamefromargv(argv)
    self.parsefileandcreatedirs(inputfilename)

# ------------------------------------------------------------------------------
def main():
  if '-r' in sys.argv:
    sys.argv.remove('-r')
    dumpdirthing = ReverseDumpDir()
  else:
    dumpdirthing = DumpDir()
  try:
    exitstatus = dumpdirthing.runexcept(sys.argv)
  except Exception as error:
    sys.stderr.write('ERROR: %s\n' % str(error))
    exitstatus = 1
  return exitstatus

# ------------------------------------------------------------------------------
if __name__ == '__main__':
  exitstatus = main()
  sys.exit(exitstatus)
