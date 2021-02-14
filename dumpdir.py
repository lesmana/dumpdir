#! /usr/bin/env python

import os
import sys
import io
import stat

# ------------------------------------------------------------------------------
class DirLine:
  def __init__(self, path):
    self.path = path

  def write(self):
    sys.stdout.write('d %s\n' % (self.path))

# ------------------------------------------------------------------------------
class SymlinkLine:
  def __init__(self, path, target):
    self.path = path
    self.target = target

  def write(self):
    sys.stdout.write('l %s\n' % (self.path))
    sys.stdout.write('> %s\n' % (self.target))


# ------------------------------------------------------------------------------
class FileLines:
  def __init__(self, path, content):
    self.path = path
    self.content = content

  def write(self):
    sys.stdout.write('f %s\n' % (self.path))
    for line in self.content:
      sys.stdout.write('> %s\n' % (line.rstrip('\n')))

# ------------------------------------------------------------------------------
class ExecFileLines:
  def __init__(self, path, content):
    self.path = path
    self.content = content

  def write(self):
    sys.stdout.write('x %s\n' % (self.path))
    for line in self.content:
      sys.stdout.write('> %s\n' % (line.rstrip('\n')))

# ------------------------------------------------------------------------------
class ReadFromFileSystem:

  def emitdir(self, path):
    linewriter = DirLine(path)
    return linewriter

  def emitlink(self, path):
    target = os.readlink(path)
    commonprefix = os.path.commonprefix([os.getcwd(), target])
    if commonprefix != '/':
      target = os.path.relpath(target)
    linewriter = SymlinkLine(path, target)
    return linewriter

  def emitexecfile(self, path):
    with open(path) as fileobject:
      content = fileobject.readlines()
    linewriter = ExecFileLines(path, content)
    return linewriter

  def emitfile(self, path):
    with open(path) as fileobject:
      content = fileobject.readlines()
    linewriter = FileLines(path, content)
    return linewriter

  def read(self):
    for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
      dirnames.sort()
      if dirpath != os.getcwd():
        relpath = os.path.relpath(dirpath)
        yield self.emitdir(relpath)
      for filename in sorted(filenames):
        dirpath_filename = os.path.join(dirpath, filename)
        relpath_filename = os.path.relpath(dirpath_filename)
        if os.path.islink(relpath_filename):
          yield self.emitlink(relpath_filename)
        elif os.access(relpath_filename, os.X_OK):
          yield self.emitexecfile(relpath_filename)
        else:
          yield self.emitfile(relpath_filename)

# ------------------------------------------------------------------------------
class DumpFileLexer:

  def linegen(self, filename):
    with open(filename) as inputfile:
      for line in inputfile:
        line = line.strip()
        if not line:
          continue
        yield line

  def tokengen(self, linegen):
    for line in linegen:
      symbol, _, content = line.partition(' ')
      yield symbol
      yield content

  def __init__(self, filename):
    self.tokensource = self.tokengen(self.linegen(filename))
    self.nexttoken = self._next()

  def _next(self):
    try:
      return next(self.tokensource)
    except StopIteration:
      return None

  def peek(self):
    return self.nexttoken

  def next(self):
    nexttoken = self.nexttoken
    self.nexttoken = self._next()
    return nexttoken

  def hasnext(self):
    return self.nexttoken is not None

# ------------------------------------------------------------------------------
class DumpFileParser:
  def __init__(self, lexer):
    self.lexer = lexer

  def adddir(self):
    name = self.lexer.next()
    dirmaker = DirMaker(name)
    return dirmaker

  def getlines(self):
    lines = io.StringIO()
    while self.lexer.hasnext():
      symbol = self.lexer.peek()
      if symbol != '>':
        break
      _ = self.lexer.next()
      content = self.lexer.next()
      lines.write(content + '\n')
    return lines

  def addfile(self):
    name = self.lexer.next()
    lines = self.getlines()
    filemaker = FileMaker(name, lines.getvalue())
    return filemaker

  def addexecfile(self):
    name = self.lexer.next()
    lines = self.getlines()
    filemaker = ExecFileMaker(name, lines.getvalue())
    return filemaker

  def addsymlink(self):
    name = self.lexer.next()
    symbol = self.lexer.next()
    assert symbol == '>'
    content = self.lexer.next()
    symlinkmaker = SymlinkMaker(name, content)
    return symlinkmaker

  def parse(self):
    symbol = self.lexer.next()
    if symbol == 'd':
      return self.adddir()
    elif symbol == 'f':
      return self.addfile()
    elif symbol == 'x':
      return self.addexecfile()
    elif symbol == 'l':
      return self.addsymlink()
    else:
      raise Exception('unknown type: %s' % symbol)


# ------------------------------------------------------------------------------
class ReadFromFile:
  def __init__(self, inputfilename):
    self.lexer = DumpFileLexer(inputfilename)
    self.parser = DumpFileParser(self.lexer)

  def read(self):
    while self.lexer.hasnext():
      maker = self.parser.parse()
      yield maker

# ------------------------------------------------------------------------------
class WriteToFile:

  def write(self, linewriter):
    linewriter.write()

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
class ExecFileMaker:
  def __init__(self, path, content):
    self.path = path
    self.content = content

  def make(self):
    with open(self.path, 'w') as fileob:
      fileob.write(self.content)
      mode = os.stat(fileob.fileno()).st_mode
      mode |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
      os.chmod(fileob.fileno(), stat.S_IMODE(mode))

# ------------------------------------------------------------------------------
class SymlinkMaker:
  def __init__(self, path, target):
    self.path = path
    self.target = target

  def make(self):
    os.symlink(self.target, self.path)

# ------------------------------------------------------------------------------
class WriteToFileSystem:

  def write(self, maker):
    maker.make()

# ------------------------------------------------------------------------------
class Runner:
  def __init__(self, reader, writer):
    self.reader = reader
    self.writer = writer

  def runexcept(self):
    for thing in self.reader.read():
      self.writer.write(thing)
    return 0

# ------------------------------------------------------------------------------
def configfromargv(argv):
  if '-r' in argv:
    argv.remove('-r')
    if len(argv) == 2:
      inputfilename = argv[1]
    else:
      raise Exception('need filename')
    reader = ReadFromFile(inputfilename)
    writer = WriteToFileSystem()
  else:
    reader = ReadFromFileSystem()
    writer = WriteToFile()
  return reader, writer

# ------------------------------------------------------------------------------
def main(argv):
  reader, writer = configfromargv(argv)
  runner = Runner(reader, writer)
  exitstatus = runner.runexcept()
  return exitstatus

# ------------------------------------------------------------------------------
if __name__ == '__main__':
  exitstatus = main(sys.argv)
  sys.exit(exitstatus)
