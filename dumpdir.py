#! /usr/bin/env python

import os

# ------------------------------------------------------------------------------
class DumpDir(object):

  def __init__(self, stdout):
    self.stdout = stdout

  def dumpdir(self):
    cwd = os.getcwd()
    for (dirpath, dirnames, filenames) in os.walk(cwd):
      dirnames.sort()
      if dirpath != cwd:
        relpath = os.path.relpath(dirpath)
        self.stdout.write('d %s\n' % (relpath))
      for filename in sorted(filenames):
        dirpath_filename = os.path.join(dirpath, filename)
        relpath_filename = os.path.relpath(dirpath_filename)
        if os.path.islink(relpath_filename):
          target = os.readlink(relpath_filename)
          commonprefix = os.path.commonprefix([cwd, target])
          if commonprefix != '/':
            target = '(...)' + os.path.relpath(target)
          self.stdout.write('l %s -> %s\n' % (relpath_filename, target))
        else:
          self.stdout.write('f %s\n' % (relpath_filename))
          with open(relpath_filename) as fileobject:
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
  dumpdir = DumpDir(sys.stdout)
  mainrunner = Main(dumpdir)
  mainrunner.run()
