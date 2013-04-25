#! /usr/bin/env python

import os

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

  def __init__(self, dumpdir):
    self.dumpdir = dumpdir

  def run(self):
    self.dumpdir.dumpdir()

# ------------------------------------------------------------------------------
def main():
  import sys
  dumpdir = DumpDir(os, open, sys.stdout)
  mainrunner = Main(dumpdir)
  mainrunner.run()
