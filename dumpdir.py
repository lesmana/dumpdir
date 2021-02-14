#! /usr/bin/env python

import os
import sys
import io
import stat

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
    dirmaker = DirLine(name)
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
    filemaker = FileLines(name, lines.getvalue())
    return filemaker

  def addexecfile(self):
    name = self.lexer.next()
    lines = self.getlines()
    filemaker = ExecFileLines(name, lines.getvalue())
    return filemaker

  def addsymlink(self):
    name = self.lexer.next()
    symbol = self.lexer.next()
    assert symbol == '>'
    content = self.lexer.next()
    symlinkmaker = SymlinkLine(name, content)
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
class DirLine:
  def __init__(self, path):
    self.path = path

  def writetofile(self, writer):
    writer.writedir(self.path)

  def writetofilesystem(self, writer):
    writer.writedir(self.path)

# ------------------------------------------------------------------------------
class SymlinkLine:
  def __init__(self, path, target):
    self.path = path
    self.target = target

  def writetofile(self, writer):
    writer.writesymlink(self.target, self.path)

  def writetofilesystem(self, writer):
    writer.writesymlink(self.target, self.path)

# ------------------------------------------------------------------------------
class FileLines:
  def __init__(self, path, content):
    self.path = path
    self.content = content

  def writetofile(self, writer):
    writer.writefile(self.path, self.content)

  def writetofilesystem(self, writer):
    writer.writefile(self.path, self.content)

# ------------------------------------------------------------------------------
class ExecFileLines:
  def __init__(self, path, content):
    self.path = path
    self.content = content

  def writetofile(self, writer):
    writer.writeexecfile(self.path, self.content)

  def writetofilesystem(self, writer):
    writer.writeexecfile(self.path, self.content)

# ------------------------------------------------------------------------------
class WriteToFile:

  def writedir(self, path):
    sys.stdout.write('d %s\n' % (path))

  def writesymlink(self, target, path):
    sys.stdout.write('l %s\n' % (path))
    sys.stdout.write('> %s\n' % (target))

  def writefile(self, path, content):
    sys.stdout.write('f %s\n' % (path))
    for line in content:
      sys.stdout.write('> %s\n' % (line.rstrip('\n')))

  def writeexecfile(self, path, content):
    sys.stdout.write('x %s\n' % (path))
    for line in content:
      sys.stdout.write('> %s\n' % (line.rstrip('\n')))

  def write(self, thing):
    thing.writetofile(self)

# ------------------------------------------------------------------------------
class WriteToFileSystem:

  def writedir(self, path):
    os.mkdir(path)

  def writefile(self, path, content):
    with open(path, 'w') as fileob:
      fileob.write(content)

  def writeexecfile(self, path, content):
    with open(path, 'w') as fileob:
      fileob.write(content)
      mode = os.stat(fileob.fileno()).st_mode
      mode |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
      os.chmod(fileob.fileno(), stat.S_IMODE(mode))

  def writesymlink(self, target, path):
    os.symlink(target, path)

  def write(self, thing):
    thing.writetofilesystem(self)

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
