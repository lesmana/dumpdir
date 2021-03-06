#! /usr/bin/env python

import os
import sys
import io
import stat
import contextlib

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
  def __init__(self, _):
    pass

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
  def __init__(self, _):
    pass

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

  def tokengen(self, fileob):
    while True:
      line = fileob.readline()
      if line == '':
        break
      if line == '\n':
        continue
      line = line.rstrip('\n')
      symbol, _, content = line.partition(' ')
      yield symbol
      yield content

  def __init__(self, fileob):
    self.tokensource = self.tokengen(fileob)
    self.nexttoken = None
    self._hasnext = None
    self._next()

  def _next(self):
    try:
      self.nexttoken = next(self.tokensource)
    except StopIteration:
      self._hasnext = False
    else:
      self._hasnext = True

  def peek(self):
    return self.nexttoken

  def next(self):
    nexttoken = self.nexttoken
    self._next()
    return nexttoken

  def hasnext(self):
    return self._hasnext

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
  def __init__(self, fileob):
    self.fileob = fileob

  def read(self):
    lexer = DumpFileLexer(self.fileob)
    parser = DumpFileParser(lexer)
    while lexer.hasnext():
      data = parser.parse()
      yield data

# ------------------------------------------------------------------------------
class WriteToFile:
  def __init__(self, outfile):
    self.outfile = outfile

  def writedir(self, path):
    self.outfile.write('d %s\n' % (path))

  def writesymlink(self, target, path):
    self.outfile.write('l %s\n' % (path))
    self.outfile.write('> %s\n' % (target))

  def writefile(self, path, content):
    self.outfile.write('f %s\n' % (path))
    for line in content:
      self.outfile.write('> %s\n' % (line.rstrip('\n')))

  def writeexecfile(self, path, content):
    self.outfile.write('x %s\n' % (path))
    for line in content:
      self.outfile.write('> %s\n' % (line.rstrip('\n')))

  def write(self, data):
    data.doubledispatch(self)

# ------------------------------------------------------------------------------
class OpenFileContext:
  def __init__(self, filename, mode):
    self.filename = filename
    self.mode = mode
    self.fileob = None

  @contextlib.contextmanager
  def __call__(self):
    fileob = open(self.filename, self.mode)
    try:
      yield fileob
    finally:
      fileob.close()

# ------------------------------------------------------------------------------
class StdContext:
  def __init__(self, stdstream):
    self.stdstream = stdstream

  @contextlib.contextmanager
  def __call__(self):
    try:
      yield self.stdstream
    finally:
      pass

# ------------------------------------------------------------------------------
class NoneContext:

  @contextlib.contextmanager
  def __call__(self):
    try:
      yield
    finally:
      pass

# ------------------------------------------------------------------------------
class Runner:
  def __init__(self, readercls, infilectx, writercls, outfilectx):
    self.readercls = readercls
    self.infilectx = infilectx
    self.writercls = writercls
    self.outfilectx = outfilectx

  def runcontext(self, infile, outfile):
    reader = self.readercls(infile)
    writer = self.writercls(outfile)
    for data in reader.read():
      writer.write(data)

  def runexcept(self):
    with self.infilectx() as infile:
      with self.outfilectx() as outfile:
        self.runcontext(infile, outfile)
    return 0

# ------------------------------------------------------------------------------
def configfromargv(argv):
  if '-r' in argv:
    argv.remove('-r')
    if len(argv) == 2:
      inputfilename = argv[1]
    else:
      raise Exception('need filename')
    readercls = ReadFromFile
    infilectx = OpenFileContext(inputfilename, 'r')
    writercls = WriteToFileSystem
    outfilectx = NoneContext()
  else:
    readercls = ReadFromFileSystem
    infilectx = NoneContext()
    writercls = WriteToFile
    outfilectx = StdContext(sys.stdout)
  runner = Runner(readercls, infilectx, writercls, outfilectx)
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
