#! /usr/bin/env python

import os

# ------------------------------------------------------------------------------
def main():
  cwd = os.getcwd()
  for (dirpath, dirnames, filenames) in os.walk(cwd):
    if dirpath == cwd:
      basename = os.path.basename(dirpath)
      print "%s" % (basename)
      if not dirnames and not filenames:
        print "(empty)"
    else:
      relpath = os.path.relpath(dirpath)
      print "d %s" % (relpath)
    for filename in filenames:
      dirpath_filename = os.path.join(dirpath, filename)
      relpath_filename = os.path.relpath(dirpath_filename)
      if os.path.islink(relpath_filename):
        target = os.readlink(relpath_filename)
        print "l %s -> %s" % (relpath_filename, target)
      else:
        print "f %s" % (relpath_filename)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
  main()
