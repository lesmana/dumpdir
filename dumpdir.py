#! /usr/bin/env python

import os
import sys
import io

# ------------------------------------------------------------------------------
class DirLine:
  def __init__(self, path):
    self.path = path

  def write(self):
    sys.stdout.write('d %s\n' % (self.path))

# ------------------------------------------------------------------------------
class SymlinkLine:
  def __init__(self, path):
    self.path = path

  def write(self):
    target = os.readlink(self.path)
    commonprefix = os.path.commonprefix([os.getcwd(), target])
    if commonprefix != '/':
      target = os.path.relpath(target)
    sys.stdout.write('l %s\n' % (self.path))
    sys.stdout.write('> %s\n' % (target))


# ------------------------------------------------------------------------------
class FileLines:
  def __init__(self, path):
    self.path = path

  def write(self):
    sys.stdout.write('f %s\n' % (self.path))
    with open(self.path) as fileobject:
      for line in fileobject:
        sys.stdout.write('> %s\n' % (line.rstrip('\n')))

# ------------------------------------------------------------------------------
class DumpFileWriter:

  def add(self, linewriter):
    linewriter.write()

# ------------------------------------------------------------------------------
class DumpDir(object):

  def source(self):
    for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
      dirnames.sort()
      if dirpath != os.getcwd():
        relpath = os.path.relpath(dirpath)
        linewriter = DirLine(relpath)
        yield linewriter
      for filename in sorted(filenames):
        dirpath_filename = os.path.join(dirpath, filename)
        relpath_filename = os.path.relpath(dirpath_filename)
        if os.path.islink(relpath_filename):
          linewriter = SymlinkLine(relpath_filename)
          yield linewriter
        else:
          linewriter = FileLines(relpath_filename)
          yield linewriter

  def runexcept(self):
    dumpfilewriter = DumpFileWriter()
    for linewriter in self.source():
      dumpfilewriter.add(linewriter)

# ------------------------------------------------------------------------------
class DirMaker:
  def __init__(self, path):
    self.path = path

  def make(self):
    os.mkdir(self.path)

# ------------------------------------------------------------------------------
class FileMaker:
  def __init__(self, path, content):
    self.path = path
    self.content = content

  def make(self):
    with open(self.path, 'w') as fileob:
      fileob.write(self.content)

# ------------------------------------------------------------------------------
class SymlinkMaker:
  def __init__(self, path, target):
    self.path = path
    self.target = target

  def make(self):
    os.symlink(self.target, self.path)

# ------------------------------------------------------------------------------
class FileBuilder:
  def __init__(self, path):
    self.path = path
    self.content = io.StringIO()

  def addline(self, line):
    self.content.write(line + '\n')

  def build(self):
    filemaker = FileMaker(self.path, self.content.getvalue())
    return filemaker

# ------------------------------------------------------------------------------
class SymlinkBuilder:
  def __init__(self, path):
    self.path = path
    self.target = None

  def addline(self, target):
    if self.target is not None:
      raise Exception(f'this symlink already has target {self.path} -> {self.target}')
    self.target = target

  def build(self):
    if self.target is None:
      raise Exception(f'this symlink has no target {self.path}')
    symlinkmaker = SymlinkMaker(self.path, self.target)
    return symlinkmaker

# ------------------------------------------------------------------------------
class FileSystemSink:
  def __init__(self):
    self.filebuilder = None

  def maybewritefile(self):
    if self.filebuilder is not None:
      filemaker = self.filebuilder.build();
      yield filemaker
      self.filebuilder = None

  def adddir(self, name):
    yield from self.maybewritefile()
    dirmaker = DirMaker(name)
    yield dirmaker

  def addfile(self, name):
    yield from self.maybewritefile()
    self.filebuilder = FileBuilder(name)

  def addline(self, line):
    self.filebuilder.addline(line)

  def addsymlink(self, name):
    yield from self.maybewritefile()
    self.filebuilder = SymlinkBuilder(name)

  def done(self):
    yield from self.maybewritefile()

# ------------------------------------------------------------------------------
class ReverseDumpDir(object):

  def __init__(self, inputfilename):
    self.inputfilename = inputfilename

  def source(self):
    with open(self.inputfilename) as inputfile:
      for line in inputfile:
        line = line.strip()
        if not line:
          continue
        otype, _, content = line.partition(' ')
        yield otype, content

  def makemaker(self):
    sink = FileSystemSink()
    for otype, content in self.source():
      if otype == 'd':
        yield from sink.adddir(content)
      elif otype == 'f':
        yield from sink.addfile(content)
      elif otype == '>':
        sink.addline(content)
      elif otype == 'l':
        yield from sink.addsymlink(content)
      else:
        raise Exception('unknown type: %s' % otype)
    yield from sink.done()

  def runexcept(self):
    for maker in self.makemaker():
      maker.make()

# ------------------------------------------------------------------------------
def filenamefromargv(argv):
  if len(argv) == 2:
    inputfilename = argv[1]
  else:
    raise Exception('need filename')
  return inputfilename

# ------------------------------------------------------------------------------
def main(argv):
  if '-r' in argv:
    argv.remove('-r')
    inputfilename = filenamefromargv(argv)
    dumpdirthing = ReverseDumpDir(inputfilename)
  else:
    dumpdirthing = DumpDir()
  try:
    exitstatus = dumpdirthing.runexcept()
  except Exception as error:
    sys.stderr.write('ERROR: %s\n' % str(error))
    exitstatus = 1
  return exitstatus

# ------------------------------------------------------------------------------
if __name__ == '__main__':
  exitstatus = main(sys.argv)
  sys.exit(exitstatus)
