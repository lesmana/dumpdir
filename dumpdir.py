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
class DumpFileLexer:

  def source(self):
    with open(self.inputfilename) as inputfile:
      for line in inputfile:
        line = line.strip()
        if not line:
          continue
        symbol, _, content = line.partition(' ')
        yield symbol, content

  def __init__(self, inputfilename):
    self.inputfilename = inputfilename
    self.sauce = self.source()
    self.nextitem = self._next()

  def _next(self):
    try:
      return next(self.sauce)
    except StopIteration:
      return None

  def peek(self):
    return self.nextitem

  def next(self):
    nextitem = self.nextitem
    self.nextitem = self._next()
    return nextitem

  def hasnext(self):
    return self.nextitem is not None

# ------------------------------------------------------------------------------
class ReverseDumpDir(object):

  def __init__(self, inputfilename):
    self.inputfilename = inputfilename

  def adddir(self, name):
    dirmaker = DirMaker(name)
    return dirmaker

  def addfile(self, name, lexer):
    lines = io.StringIO()
    while lexer.hasnext():
      symbol, _ = lexer.peek()
      if symbol != '>':
        break
      _, content = lexer.next()
      lines.write(content + '\n')
    filemaker = FileMaker(name, lines.getvalue())
    return filemaker

  def addsymlink(self, name, lexer):
    symbol, content = lexer.next()
    assert symbol == '>'
    symlinkmaker = SymlinkMaker(name, content)
    return symlinkmaker

  def parse(self, lexer):
    symbol, content = lexer.next()
    if symbol == 'd':
      return self.adddir(content)
    elif symbol == 'f':
      return self.addfile(content, lexer)
    elif symbol == 'l':
      return self.addsymlink(content, lexer)
    else:
      raise Exception('unknown type: %s' % symbol)

  def runexcept(self):
    lexer = DumpFileLexer(self.inputfilename)
    while lexer.hasnext():
      maker = self.parse(lexer)
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
