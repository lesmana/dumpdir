#! /usr/bin/env python

import os

# ------------------------------------------------------------------------------
def main():
  cwd = os.getcwd()
  for (dirpath, dirnames, filenames) in os.walk(cwd):
    dirnames.sort()
    if dirpath != cwd:
      relpath = os.path.relpath(dirpath)
      print "d %s" % (relpath)
    for filename in sorted(filenames):
      dirpath_filename = os.path.join(dirpath, filename)
      relpath_filename = os.path.relpath(dirpath_filename)
      if os.path.islink(relpath_filename):
        target = os.readlink(relpath_filename)
        commonprefix = os.path.commonprefix([cwd, target])
        if commonprefix != '/':
          target = '(...)' + os.path.relpath(target)
        print "l %s -> %s" % (relpath_filename, target)
      else:
        print "f %s" % (relpath_filename)
        with open(relpath_filename) as fileobject:
          for line in fileobject:
            print "> %s" % (line.rstrip('\n'))
