#! /usr/bin/env python

import os
import sys
import io

# ------------------------------------------------------------------------------
class Dir:
  def __init__(self, path):
    self.path = path

  def tostring(self):
    sys.stdout.write('d %s\n' % (self.path))

# ------------------------------------------------------------------------------
class Symlink:
  def __init__(self, path):
    self.path = path

  def tostring(self):
    target = os.readlink(self.path)
    commonprefix = os.path.commonprefix([os.getcwd(), target])
    if commonprefix != '/':
      target = '(...)' + os.path.relpath(target)
    sys.stdout.write('l %s -> %s\n' % (self.path, target))


# ------------------------------------------------------------------------------
class File:
  def __init__(self, path):
    self.path = path

  def tostring(self):
    sys.stdout.write('f %s\n' % (self.path))
    with open(self.path) as fileobject:
      for line in fileobject:
        sys.stdout.write('> %s\n' % (line.rstrip('\n')))

# ------------------------------------------------------------------------------
class FileSink:

  def sink(self, fsob):
    fsob.tostring()

# ------------------------------------------------------------------------------
class DumpDir(object):

  def source(self):
    for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
      dirnames.sort()
      if dirpath != os.getcwd():
        relpath = os.path.relpath(dirpath)
        fsob = Dir(relpath)
        yield fsob
      for filename in sorted(filenames):
        dirpath_filename = os.path.join(dirpath, filename)
        relpath_filename = os.path.relpath(dirpath_filename)
        if os.path.islink(relpath_filename):
          fsob = Symlink(relpath_filename)
          yield fsob
        else:
          fsob = File(relpath_filename)
          yield fsob


  def dumpdir(self):
    sink = FileSink()
    for fsob in self.source():
      sink.sink(fsob)

  def runexcept(self, argv):
    self.dumpdir()

# ------------------------------------------------------------------------------
class FileBuilder:
  def __init__(self, path):
    self.path = path
    self.content = io.StringIO()

  def addline(self, line):
    self.content.write(line + '\n')

  def build(self):
    with open(self.path, 'w') as fileob:
      fileob.write(self.content.getvalue())

# ------------------------------------------------------------------------------
class FileSystemSink:
  def __init__(self):
    self.currentfile = None

  def maybewritefile(self):
    if self.currentfile is not None:
      self.currentfile.build();
      self.currentfile = None

  def adddir(self, name):
    self.maybewritefile()
    os.mkdir(name)

  def addfile(self, name):
    self.maybewritefile()
    self.currentfile = FileBuilder(name)

  def addline(self, name):
    self.currentfile.addline(name)

  def done(self):
    self.maybewritefile()

# ------------------------------------------------------------------------------
class ReverseDumpDir(object):

  def filenamefromargv(self, argv):
    if len(argv) == 2:
      inputfilename = argv[1]
    else:
      raise Exception('need filename')
    return inputfilename

  def reversedumpdir(self, inputfile):
    sink = FileSystemSink()
    for line in inputfile:
      line = line.strip()
      if not line:
        continue
      otype, _, content = line.partition(' ')
      if otype == 'd':
        sink.adddir(content)
      elif otype == 'f':
        sink.addfile(content)
      elif otype == '>':
        sink.addline(content)
      else:
        raise Exception('unknown type: %s' % otype)
    sink.done()

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
