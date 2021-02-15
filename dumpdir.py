#! /usr/bin/env python

import os
import sys
import io
import stat

# ------------------------------------------------------------------------------
class DirData:
  def __init__(self, path):
    self.path = path

  def doubledispatch(self, writer):
    writer.writedir(self.path)

# ------------------------------------------------------------------------------
class SymlinkData:
  def __init__(self, path, target):
    self.path = path
    self.target = target

  def doubledispatch(self, writer):
    writer.writesymlink(self.target, self.path)

# ------------------------------------------------------------------------------
class FileData:
  def __init__(self, path, content):
    self.path = path
    self.content = content

  def doubledispatch(self, writer):
    writer.writefile(self.path, self.content)

# ------------------------------------------------------------------------------
class ExecFileData:
  def __init__(self, path, content):
    self.path = path
    self.content = content

  def doubledispatch(self, writer):
    writer.writeexecfile(self.path, self.content)

# ------------------------------------------------------------------------------
class ReadFromFileSystem:

  def getdirdata(self, path):
    dirdata = DirData(path)
    return dirdata

  def getsymlinkdata(self, path):
    target = os.readlink(path)
    commonprefix = os.path.commonprefix([os.getcwd(), target])
    if commonprefix != '/':
      target = os.path.relpath(target)
    symlinkdata = SymlinkData(path, target)
    return symlinkdata

  def getexecfiledata(self, path):
    with open(path) as fileobject:
      content = fileobject.readlines()
    execfiledata = ExecFileData(path, content)
    return execfiledata

  def getfiledata(self, path):
    with open(path) as fileobject:
      content = fileobject.readlines()
    filedata = FileData(path, content)
    return filedata

  def read(self):
    for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
      dirnames.sort()
      if dirpath != os.getcwd():
        relpath = os.path.relpath(dirpath)
        yield self.getdirdata(relpath)
      for filename in sorted(filenames):
        dirpath_filename = os.path.join(dirpath, filename)
        relpath_filename = os.path.relpath(dirpath_filename)
        if os.path.islink(relpath_filename):
          yield self.getsymlinkdata(relpath_filename)
        elif os.access(relpath_filename, os.X_OK):
          yield self.getexecfiledata(relpath_filename)
        else:
          yield self.getfiledata(relpath_filename)

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

  def write(self, data):
    data.doubledispatch(self)

# ------------------------------------------------------------------------------
class DumpFileLexer:

  def tokengen(self, linegen):
    for line in linegen:
      symbol, _, content = line.partition(' ')
      yield symbol
      yield content

  def __init__(self, linegen):
    self.tokensource = self.tokengen(linegen)
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

  def getdirdata(self):
    name = self.lexer.next()
    dirdata = DirData(name)
    return dirdata

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

  def getfiledata(self):
    name = self.lexer.next()
    lines = self.getlines()
    filedata = FileData(name, lines.getvalue())
    return filedata

  def getexecfiledata(self):
    name = self.lexer.next()
    lines = self.getlines()
    execfiledata = ExecFileData(name, lines.getvalue())
    return execfiledata

  def getsymlinkdata(self):
    name = self.lexer.next()
    symbol = self.lexer.next()
    assert symbol == '>'
    content = self.lexer.next()
    symlinkdata = SymlinkData(name, content)
    return symlinkdata

  def parse(self):
    symbol = self.lexer.next()
    if symbol == 'd':
      return self.getdirdata()
    elif symbol == 'f':
      return self.getfiledata()
    elif symbol == 'x':
      return self.getexecfiledata()
    elif symbol == 'l':
      return self.getsymlinkdata()
    else:
      raise Exception('unknown type: %s' % symbol)


# ------------------------------------------------------------------------------
class ReadFromFile:

  def __init__(self, inputfilename):
    self.inputfilename = inputfilename

  def linegen(self, filename):
    with open(filename) as inputfile:
      for line in inputfile:
        line = line.strip()
        if not line:
          continue
        yield line

  def read(self):
    lexer = DumpFileLexer(self.linegen(self.inputfilename))
    parser = DumpFileParser(lexer)
    while lexer.hasnext():
      data = parser.parse()
      yield data

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

  def write(self, data):
    data.doubledispatch(self)

# ------------------------------------------------------------------------------
class Runner:
  def __init__(self, reader, writer):
    self.reader = reader
    self.writer = writer

  def runexcept(self):
    for data in self.reader.read():
      self.writer.write(data)
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
  runner = Runner(reader, writer)
  return runner

# ------------------------------------------------------------------------------
def main(argv):
  runner = configfromargv(argv)
  exitstatus = runner.runexcept()
  return exitstatus

# ------------------------------------------------------------------------------
if __name__ == '__main__':
  exitstatus = main(sys.argv)
  sys.exit(exitstatus)
