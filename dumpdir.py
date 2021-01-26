#! /usr/bin/env python

import os
import sys
import io

class Dir:
  def __init__(self, path):
    self.path = path

  def __str__(self):
    out = io.StringIO()
    out.write('d %s\n' % (self.path))
    return out.getvalue()

class Symlink:
  def __init__(self, path, cwd):
    self.path = path
    self.cwd = cwd

  def __str__(self):
    out = io.StringIO()
    target = os.readlink(self.path)
    commonprefix = os.path.commonprefix([self.cwd, target])
    if commonprefix != '/':
      target = '(...)' + os.path.relpath(target)
    out.write('l %s -> %s\n' % (self.path, target))
    return out.getvalue()


class File:
  def __init__(self, path):
    self.path = path

  def __str__(self):
    out = io.StringIO()
    out.write('f %s\n' % (self.path))
    with open(self.path) as fileobject:
      for line in fileobject:
        out.write('> %s\n' % (line.rstrip('\n')))
    return out.getvalue()

class FileSink:

  def __init__(self, target):
    self.target = target

  def sink(self, fsob):
    self.target.write(str(fsob))

# ------------------------------------------------------------------------------
class DumpDir(object):

  def dumpdir(self):
    sink = FileSink(sys.stdout)
    cwd = os.getcwd()
    for (dirpath, dirnames, filenames) in os.walk(cwd):
      dirnames.sort()
      if dirpath != cwd:
        relpath = os.path.relpath(dirpath)
        fsob = Dir(relpath)
        sink.sink(fsob)
      for filename in sorted(filenames):
        dirpath_filename = os.path.join(dirpath, filename)
        relpath_filename = os.path.relpath(dirpath_filename)
        if os.path.islink(relpath_filename):
          fsob = Symlink(relpath_filename, cwd)
          sink.sink(fsob)
        else:
          fsob = File(relpath_filename)
          sink.sink(fsob)

  def runexcept(self, argv):
    self.dumpdir()

# ------------------------------------------------------------------------------
class ReverseDumpDir(object):

  def filenamefromargv(self, argv):
    if len(argv) == 2:
      inputfilename = argv[1]
    else:
      raise Exception('need filename')
    return inputfilename

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

  def parsefileandcreatedirs(self, inputfilename):
    with open(inputfilename) as inputfile:
      self.reversedumpdir(inputfile)

  def runexcept(self, argv):
    inputfilename = self.filenamefromargv(argv)
    self.parsefileandcreatedirs(inputfilename)

# ------------------------------------------------------------------------------
def main(argv):
  if '-r' in argv:
    argv.remove('-r')
    dumpdirthing = ReverseDumpDir()
  else:
    dumpdirthing = DumpDir()
  try:
    exitstatus = dumpdirthing.runexcept(argv)
  except Exception as error:
    sys.stderr.write('ERROR: %s\n' % str(error))
    exitstatus = 1
  return exitstatus

# ------------------------------------------------------------------------------
if __name__ == '__main__':
  exitstatus = main(sys.argv)
  sys.exit(exitstatus)
