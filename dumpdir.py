#! /usr/bin/env python2

# ------------------------------------------------------------------------------
class DumpDir(object):

  def __init__(self, osmod, openfunc, stdout):
    self.osmod = osmod
    self.openfunc = openfunc
    self.stdout = stdout

  def dumpdir(self):
    cwd = self.osmod.getcwd()
    for (dirpath, dirnames, filenames) in self.osmod.walk(cwd):
      dirnames.sort()
      if dirpath != cwd:
        relpath = self.osmod.path.relpath(dirpath)
        self.stdout.write('d %s\n' % (relpath))
      for filename in sorted(filenames):
        dirpath_filename = self.osmod.path.join(dirpath, filename)
        relpath_filename = self.osmod.path.relpath(dirpath_filename)
        if self.osmod.path.islink(relpath_filename):
          target = self.osmod.readlink(relpath_filename)
          commonprefix = self.osmod.path.commonprefix([cwd, target])
          if commonprefix != '/':
            target = '(...)' + self.osmod.path.relpath(target)
          self.stdout.write('l %s -> %s\n' % (relpath_filename, target))
        else:
          self.stdout.write('f %s\n' % (relpath_filename))
          with self.openfunc(relpath_filename) as fileobject:
            for line in fileobject:
              self.stdout.write('> %s\n' % (line.rstrip('\n')))

# ------------------------------------------------------------------------------
class Main(object):

  def __init__(self, dumpdir, stdout):
    self.dumpdir = dumpdir
    self.stdout = stdout

  def runexcept(self):
    self.dumpdir.dumpdir()

  def run(self):
    try:
      self.runexcept()
      return 0
    except Exception as error:
      self.stdout.write('ERROR: %s\n' % str(error))
      return 1

# ------------------------------------------------------------------------------
def main():
  import os
  import sys
  dumpdir = DumpDir(os, open, sys.stdout)
  mainrunner = Main(dumpdir, sys.stdout)
  exitstatus = mainrunner.run()
  sys.exit(exitstatus)

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
        self.osmod.mkdir(name)
      elif type == 'f':
        currentfilename = name
        currentfile = self.openfunc(currentfilename, 'w')
        currentfile.close()
      elif type == '>':
        currentfile = self.openfunc(currentfilename, 'a')
        currentfile.write(name + '\n')
        currentfile.close()
      else:
        raise Exception('unknown type: %s' % type)

# ------------------------------------------------------------------------------
class ReverseMain(object):

  def __init__(self, reversedumpdir, stdout):
    self.reversedumpdir = reversedumpdir
    self.stdout = stdout

  def filenamefromargv(self, argv):
    if len(argv) == 2:
      inputfilename = argv[1]
    else:
      raise Exception('need filename')
    return inputfilename

  def parsefileandcreatedirs(self, inputfilename):
    with open(inputfilename) as inputfile:
      self.reversedumpdir.reversedumpdir(inputfile)

  def runexcept(self, argv):
    inputfilename = self.filenamefromargv(argv)
    self.parsefileandcreatedirs(inputfilename)

  def run(self, argv):
    try:
      self.runexcept(argv)
      return 0
    except Exception as error:
      self.stdout.write('ERROR: %s\n' % str(error))
      return 1

# ------------------------------------------------------------------------------
def reversemain():
  import os
  import sys
  reversedumpdir = ReverseDumpDir(os, open)
  mainrunner = ReverseMain(reversedumpdir, sys.stdout)
  exitstatus = mainrunner.run(sys.argv)
  sys.exit(exitstatus)
